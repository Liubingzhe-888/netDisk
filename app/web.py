
from app.utils.size_format import size_format
from app.utils.loginCheck import login_required
from app.model import File, Share
from flask import Blueprint, render_template,abort


web = Blueprint('web', __name__, static_folder='static')
from app.setting import SAVE_PATH
@web.route('/index')
@login_required
def index():
    file = File.query.all()
    return render_template('index.html',
    total=len(file),
    size=size_format(sum([i.file_size for i in file if i.file_type!='dir'])),
    path=SAVE_PATH)


@web.route('/upload/<int:file_id>')
@login_required
def upload(file_id):
    try:
        if file_id==0:
            return render_template('upload.html',name="根目录") 
        file = File.query.get(file_id)
        return render_template('upload.html',name=file.file_name)
    except:
        abort(404)

@web.route('/share/<id>')
def share(id):
    file = File.query.get(int(id))
    if file.file_type!='dir':
        return render_template('share.html',
        file_name=file.file_name,
        file_size=size_format(file.file_size),
        file_id=file.id)
    else:
        return render_template('404.html',
        error="文件夹暂不支持分享！",
        file_size="",
        file_id=file.id)


@web.route('/share/admin')
@login_required
def share_admin_page():
    """
    查询所有分享链接
    前后端未分离
    """
    share_file = Share.query.all()
    return render_template('shareAdmin.html', share_file=share_file)

@web.route('/share/download/<id>')
def share_download(id):
    """
    分享文件下载页面
    """
    share_info = Share.query.filter_by(share_url=id).first()
    if share_info:
        return render_template('shareDownload.html',id=share_info.share_url)
    else:
        abort(404,"无")

@web.route('/tree')
@login_required
def tree_dir():
    return render_template('tree.html')


@web.route('/login')
def login_html():
    return render_template('login.html')


@web.route('/readme')
def readme():
    return render_template('readme.html')