from app import db


# 文件类型
class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True) # 文件id
    file_real_name = db.Column(db.Text)#文件真实名称
    file_name = db.Column(db.Text)#文件名称
    file_save_path = db.Column(db.Text)#文件储存位置
    file_create_time = db.Column(db.DateTime)#文件上传时间
    file_type = db.Column(db.String(6))#文件类型
    file_size = db.Column(db.Integer)#文件大小
    file_upload_user = db.Column(db.Text)#文件上传者
    file_superior_dir = db.Column(db.Integer)#文件目录
    file_path = db.Column(db.Text)#文件下载地址
    file_level = db.Column(db.Integer)# 文件所在层

# 分享链接
class Share(db.Model):
    __tablename__ = 'share'
    """
    分享链接id
    分享文件名称
    分享链接有效时间
    分析文件url
    链接访问次数
    链接密码
    分享文件id
    """
    id = db.Column(db.Integer, primary_key=True)
    share_file_name = db.Column(db.Text)
    share_last_time = db.Column(db.DateTime)
    share_url = db.Column(db.Text)
    share_view_time = db.Column(db.Integer)
    share_password = db.Column(db.Text)
    share_file_id = db.Column(db.Integer)


class Setting(db.Model):
    __tablename__ = 'setting'
    id = db.Column(db.Integer, primary_key=True)
    pwdHash = db.Column(db.Text)
