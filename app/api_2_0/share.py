from app.utils.loginCheck import login_required
from app.utils.size_format import size_format
from app.utils.status import CODE
from app.model import Share,File,db
from app.utils.shareFunc import get_share_password, get_uuid
import datetime
from app.utils.format_time import format_time
from app.api_2_0 import API2
from flask import request,jsonify,session
"""
文件分享功能模块
"""

@login_required
@API2.route('/file/share')
def create_share_url():
    """
    分享文件
    args:
        file_id 文件id
        end_time 分享链接时效
    """
    file_id = request.args.get('file_id')
    file_end_time = int(request.args.get('file_end_time'))
    file = File.query.filter_by(id=file_id).first()
    if file and file.file_type!='dir':
        is_share = Share.query.filter_by(share_file_name=file.file_name).first()
        if is_share:
            return jsonify(data={'msg': '已经存在该文件的分享链接',
                                 'file_name': is_share.share_file_name,
                                 'pwd': is_share.share_password,
                                 'time': format_time(is_share.share_last_time),
                                 'url': '/share/file/detail/' + is_share.share_url}, 
                                 msg=f'已经存在该分享链接：<br>我分享给你了{is_share.share_file_name},\
                                 下载密码为{is_share.share_password},到期时间是{is_share.share_last_time.strftime("%Y-%m-%d %H:%M:%S")}\
                                 ,请尽快下载，下载链接为{request.host}/share/download/{is_share.share_url}',
                                 code=CODE.NOT_ALLOW)
        else:
            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(days=int(file_end_time))
            share_pwd = get_share_password()
            share_url = get_uuid()
            share_file = Share(share_file_name=file.file_name,
                               share_last_time=end_time,
                               share_url=share_url,
                               share_file_id = file.id,
                               share_view_time=0,
                               share_password=share_pwd)
            db.session.add(share_file)
            db.session.commit()
            return jsonify(msg=f'分享给你了{file.file_name},\
                            下载密码为{share_pwd},\
                            下载链接为<a>{request.host}/share/download/{share_url}</a>',
                                 code=CODE.ALLOW)
    else:
        return jsonify(code=CODE.NOT_ALLOW[0],msg='文件不存在或该文件不支持分享')
@API2.route('/file/share/download/info')
def get_share_file_info():
    url = request.args.get('share_url')
    pwd = request.args.get('pwd')
    share = Share.query.filter_by(share_url = url).first()
    if share:
        share.share_view_time= share.share_view_time+1
        db.session.add(share)
        db.session.commit()
        if share.share_password==pwd:
            file = File.query.filter_by(id=share.share_file_id).first()
            session['downloader']=True
            return jsonify(
                code=CODE.ALLOW[0],
                msg='密码正确',
                data={'file_name':file.file_name,
                'file_size':size_format(file.file_size),
                'share_last_time':format_time(share.share_last_time),
                'file_download':'/api/download/'+share.share_url})
        else:
             return jsonify(code=CODE.NOT_ALLOW[0],msg='密码错误',data='')


# 取消分享
@API2.route('/share/delete/<int:id>')
def delete_share_url(id):
    share_url = Share.query.filter_by(id=id).first()
    db.session.delete(share_url)
    db.session.commit()
    return "<h1>取消分享成功</h1>"