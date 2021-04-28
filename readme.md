# 基于Flask的网盘系统

## **安装库**

```
pip install -r requirements.txt
```

## **初始化数据库**

```
python manager.py create_db
```

## **运行**

```
python start.py
```

## **技术栈**

- 采用前后端混合开发，由flask进行模板渲染
- 数据库采用sqlite
- 前端
  - layui
  - css
  - html
  - js
- 后端
  - flask

## 实现的功能

- 文件
  - 上传、下载、在线预览（依靠浏览器渲染能力）、移动、删除、分享、新建文件夹
- 分享

## 其他

第一代版本，部分功能还没有完善，留存在这，慢慢修改。