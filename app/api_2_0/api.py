from app.utils.loginCheck import login_required
import datetime
import os
from app.api_2_0 import API2
from app.model import *
from app.setting import ALLOWUPLOAD, SAVE_PATH
from app.utils.format_time import format_time
from app.utils.shareFunc import get_share_password, get_uuid
from app.utils.size_format import size_format
from app.utils.status import CODE
from flask import jsonify, request,abort,redirect
from flask.globals import session
from flask.helpers import send_from_directory, url_for
from flask.templating import render_template

@login_required
@API2.route('/file/query/total/<int:file_id>')
def query_files(file_id):
    """
    文件查询
    file_id:文件id
    首先根据file_id 看一下它是谁的上级目录 28行
    """
    try:
            # 页数 每页显示数
            page = int(request.args.get('page',1))
            size = int(request.args.get('limit',10))
            # 根据文件id查询
            pagination = File.query.filter_by(file_superior_dir=file_id).paginate(page,per_page=size)
            file_list = pagination.items
            file_data = []
            
            for file in file_list:
                dic = {
                    'id':file.id,
                    'file_name':file.file_name,
                    'file_create_time':format_time(file.file_create_time),
                    'file_size':size_format(int(file.file_size)) if file.file_type!='dir' else '',
                    'file_superior_dir':file.file_superior_dir if file_id!=0 else 'root',
                    'file_type':file.file_type,
                    'file_upload_user':file.file_upload_user
                }
                file_data.append(dic)
                dic = {}
            father_dir = File.query.filter_by(
                id=file_id).first().file_superior_dir if file_id!=0 else 0
            return jsonify(
                code=CODE.ALLOW[0],
                data=file_data,
                now_dir=file_id,
                file_superior_dir=father_dir,
                msg='success',
                total=pagination.total)            
    except Exception as e:
        return jsonify(code=CODE.ERROR[0],
                        data='',
                        now_dir=file_id,
                        msg=str(e),
                        total=pagination.total)

# 弃用
# @API2.route('/file/delete')
# def delete_file():
#     file_id = int(request.args.get('file'))
#     file = File.query.get(file_id)
#     if file.file_type!='dir':
#         os.remove(os.path.join(SAVE_PATH,file.file_real_name))
#         db.session.delete(file)
#         db.session.commit()
#         return jsonify(code=CODE.ALLOW[0],msg='删除成功',data='')
#     else:
#         # 文件夹的数据要递归删除！
#         db.session.delete(file)
#         db.session.commit()
#         return jsonify(code=CODE.ALLOW[0],msg='删除成功',data='')        

@login_required
@API2.route('/file/delete/batch',methods=['POST'])
def delete_file_batch():
    """
    文件批量删除
    """
    try:
        file_id = request.get_json()
        for file in file_id:
            file = File.query.get(file)
            if file.file_type!='dir':
                os.remove(os.path.join(SAVE_PATH,file.file_real_name))
                db.session.delete(file)
            else:
                delete_in_dir(file.id)
                db.session.delete(file)
        db.session.commit()
        return jsonify(code=CODE.ALLOW[0],msg='删除成功',data='')
    except:
        return jsonify(code=CODE.NOT_ALLOW[0],msg='删除失败！')
# 递归删除函数
def delete_in_dir(file_name):
    belong_file = File.query.filter_by(file_superior_dir = file_name).all()
    for i in belong_file:
        if i.file_type=='dir':
            print('正在删除'+i.file_name)
            delete_in_dir(i.id)
            db.session.delete(i)
        else:
            os.remove(os.path.join(SAVE_PATH,i.file_real_name))
            db.session.delete(i)

# 文件修改名称
@login_required
@API2.route('/file/filename/change')
def change_file():
    file_name = str(request.args.get('new_file_name'))
    file_id = int(request.args.get('file_id'))
    file = File.query.filter_by(id=file_id).first()
    if file.file_type !='dir':
        file.file_name = file_name
        file.file_real_name = file_name
        p,f=os.path.split(file.file_save_path)
        os.rename(file.file_save_path,os.path.join(p,file_name))
        db.session.add(file)
        db.session.commit()
    else:
        file.file_name = file_name
        db.session.add(file)
        db.session.commit()
    return jsonify(code=CODE.ALLOW[0],msg=f'修改成功 修改为{file_name}',data='')

# 文件在线查看
@login_required
@API2.route('/view/<file_id>')
def view_file(file_id):
    file = File.query.filter_by(id=int(file_id)).first()
    if file and file.file_type!='dir':
        return send_from_directory(file.file_save_path,file.file_real_name)
    else:
        #return send_from_directory(file.file_save_path,file.file_real_name,as_attachment=True)
        return render_template('404.html', error='暂无该文件，或该文件不支持在线预览！')

# 文件上传
@login_required
@API2.route('/upload/<file_id>', methods=['POST'])
def upload(file_id):
    """
    文件的上传
    path: id
    """
    try:
        f = request.files['file']
        file_name = f.filename.replace(' ', '')
        file_type = os.path.splitext(file_name)[1]
        if file_type not in ALLOWUPLOAD:
            return jsonify(code=201,msg='上传失败，文件类型不符合')
        file_save_path = os.path.join(SAVE_PATH, file_name)
        f.save(file_save_path)
        upload_time = datetime.datetime.now()
        file_size = os.path.getsize(file_save_path)
        new_file = File(file_real_name=file_name,
                        file_name=file_name.split('.')[0],
                        file_save_path=SAVE_PATH,
                        file_create_time=upload_time,
                        file_size=file_size,
                        file_upload_user='admin',
                        file_superior_dir=file_id,
                        file_type=file_type)
        db.session.add(new_file)
        db.session.commit()
        return jsonify(code=200,msg='上传成功',data='')
    except Exception as e:
        return jsonify(code=201,msg='上传失败')

# 文件下自
@API2.route('/download/<id>/<user_type>')
def download_file(id,user_type='user'):
    """
    管理员访问id是文件id
    访客下载是分享id
    """
    try:
        if user_type=='admin':
            file = File.query.get(int(id))
            return send_from_directory(file.file_save_path,file.file_real_name,as_attachment=True)
        else:
            if session['downloader']:
                share = Share.query.filter_by(share_url = id).first()
                file = File.query.get(int(share.share_file_id))
                session['downloader']=False
                return send_from_directory(file.file_save_path,file.file_real_name,as_attachment=True)
            else:
                return '下载失败！'
    except Exception as e:
        return '<script>alert("下载失败，请检查下载文件类型是否支持下载，或密码是否正确")</script>'

#创建文件夹
@login_required
@API2.route('/create/dir')
def create_dir():
    """
    创建文件夹
    """
    file_superior_dir = request.args.get('file_superior_dir',0,int)
    new_dir_name = request.args.get('new_dir_name')
    
    if new_dir_name=='':
        return jsonify(code=CODE.NOT_ALLOW[0],data='',msg='创建失败，请输入文件夹名称')
    if ' ' in new_dir_name:
        return jsonify(code=CODE.NOT_ALLOW[0],data='',msg='创建失败，请输入文件夹名称不能含有空格')
    
    child_file = File.query.filter_by(file_superior_dir = file_superior_dir).all()
    now_dir = File.query.get(file_superior_dir)
    
    for i in child_file:
        if i.file_name == new_dir_name:
            return jsonify(code=CODE.NOT_ALLOW[0],data='',msg='创建失败，文件名重复')

    file = File(
        file_name = new_dir_name,
        file_real_name = new_dir_name,
        file_create_time = datetime.datetime.now(),
        file_type = 'dir',
        file_upload_user = 'admin',
        file_superior_dir = file_superior_dir,
        file_level  = 0 if file_superior_dir==0 else now_dir.file_level+1
        )
    db.session.add(file)
    db.session.commit()
    return jsonify(code=CODE.ALLOW[0],data='',msg=f'新建{new_dir_name}成功')

# 查询所有文件夹
@login_required
@API2.route('/file/query/total/dir')
def query_total_dir():
    first_dir = File.query.filter(File.file_type == 'dir',File.file_superior_dir==0).all()
    data_list = []
    for one_dir in first_dir:
        data = {'title':one_dir.file_name,
        'id':one_dir.id,
        'field':one_dir.id,
        'checked':'',
        'spread':'',
        'children':query_total_dir_in(one_dir.id)}
        data_list.append(data)
        data = {}
    return jsonify(data=data_list)

# 文件移动
@login_required
@API2.route('/file/move')
def move_file():
    file_id = request.args.get('file_id',None)
    to_file_id = request.args.get('to_file_id',None)
    moveing_file = File.query.get(file_id)
    to_file = File.query.filter_by(file_superior_dir=to_file_id).all()
    if to_file:
        for i in to_file:
            if i.file_name == moveing_file.file_name:
                return jsonify(msg='移动失败，该文件夹下有重复文件名称！')
    moveing_file.file_superior_dir = to_file_id
    db.session.add(moveing_file)
    db.session.commit()
    return jsonify(code=CODE.ALLOW[0],msg='成功',data='')

# 递归文件夹树
def query_total_dir_in(dir_id):
    dir_ = File.query.filter(File.file_superior_dir == dir_id,File.file_type=='dir').all()
    if dir_:
        data_list = []
        for i in dir_:
            data = {'title':i.file_name,
            'id':i.id,
            'field':i.id,
            'checked':'',
            'spread':'',
            'children':query_total_dir_in(i.id)}
            data_list.append(data)
            data = {}
        return data_list
    else:
        return []

