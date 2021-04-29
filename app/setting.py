from app.web import web
import os
# 保存的文件格式
SAVE_PATH = os.path.join(web.static_folder, "file")
# 允许上传的文件格式
# 可以在论文描述 作为论文内容
# 比如：网盘提供了文件类型限制上传功能，旨在保证了非法文件的上传。
ALLOWUPLOAD = ['.txt','.pdf','.doc','.docx','mp3','mp4','ppt','.zip','.rar','.jpg','.png','.jar']

"""
设置网盘账号密码
"""
USERNAME='666'
PASSWORD='123456'