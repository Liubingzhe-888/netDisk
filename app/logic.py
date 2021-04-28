from flask import Blueprint, g
import datetime
import os
from flask import render_template, session, request, jsonify, abort, send_from_directory
from app import db
from app.model import File, Share, Setting
from app.utils.size_format import size_format
from app.utils.status import CODE as code
from werkzeug.security import generate_password_hash,check_password_hash

logic = Blueprint('logic', __name__, static_folder='static/file')


@logic.route('/login', methods=['POST'])
def login():
    """
    登陆接口
    """
    password = request.json
    right_pwd = Setting.query.filter_by(id=1).first()
    is_ok = check_password_hash(right_pwd.pwdHash, str(password))
    if is_ok:
        session['user'] = right_pwd.pwdHash
        g.user = session['user']
        return jsonify({'status': code.ALLOW, 'redirect': '/'})
    else:
        return jsonify({'status': code.NOT_ACCEPT})


# @logic.route('/view/<file_id>', methods=['GET'])
# def view_file(file_id):
#     if file_id:
#         file = File.query.filter_by(id=file_id).first()
#         print(file.file_name)
#         if file:
#             return logic.send_static_file(file.file_real_name)
#         else:
#             return render_template('404.html', text='暂无该文件')
#     else:
#         return render_template('404.html', text='error')


@logic.route('/pwd/<pwd>')
def set_pwd(pwd):
    now_pwd = Setting.query.filter_by(id=1).first()
    if now_pwd:
        now_pwd.pwdHash = generate_password_hash(pwd)
        db.session.add(now_pwd)
        db.session.commit()
        session.clear()
        return '密码设置成功！'
    else: # 如果没有密码则
        new_pwd = Setting(pwdHash=generate_password_hash(pwd))
        db.session.add(new_pwd)
        db.session.commit()
        return '密码设置成功！'


@logic.route('/share/file/detail/<file_id>', methods=['GET'])
def return_share_template(file_id):
    """
    放问分享链接url 面向访客
    如果文件不存在则404
    """
    session['visitor'] = None
    share_file = Share.query.filter_by(share_url=file_id).first()
    if share_file:
        file = File.query.filter_by(file_name=share_file.share_file_name).first()
        if file:
            now_time = datetime.datetime.now()
            now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
            d1 = datetime.datetime.strptime(share_file.share_last_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            d2 = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
            if (d1 - d2).days > 0:
                return render_template('shareDownload.html')
            else:
                db.session.delete(share_file)
                db.session.commit()
                abort(404)
        else:
            db.session.delete(share_file)
            db.session.commit()
            abort(404)
    else:
        abort(404)


# 访客获取分享文件
@logic.route('/share/file/detail/<file_id>', methods=['POST'])
def get_share_file_info(file_id):
    """
    POST请求
    提交密码 返回文件信息
    """
    share_file = Share.query.filter_by(share_url=file_id).first()
    share_pwd = request.json['pwd']
    if share_pwd == share_file.share_password:
        file = File.query.filter_by(file_name=share_file.share_file_name).first()
        if file:
            session['visitor'] = share_pwd
            return jsonify(data={'file_name': file.file_name,
                                 'file_size': size_format(int(file.file_size)),
                                 'file_download': file.id},
                           code=code.ALLOW)
        else:
            return jsonify(data='暂无此文件，可能已经被删除', code=code.NOT_ALLOW)
    else:
        return jsonify(data='密码错误或者该文件已经被删除！', code=code.NOT_ALLOW)


# 访客下载分享的文件
@logic.route("/share/download/file/<int:file_id>", methods=['GET'])
def download(file_id):
    """
    分享文件下载
    面向访客
    """
    if session['visitor'] is None:
        print("未输入密码不可访问!")
        abort(404)
    else:
        file = File.query.filter_by(id=file_id).first()
        download_path = os.path.split(file.file_save_path)[0]
        file_name = file.file_name
        return send_from_directory(download_path, filename=file_name, as_attachment=True)


# 取消分享
@logic.route('/share/delete/<int:id>')
def delete_share_url(id):
    share_url = Share.query.filter_by(id=id).first()
    db.session.delete(share_url)
    db.session.commit()
    return "success"
