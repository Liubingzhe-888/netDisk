from app.utils.loginCheck import login_required
from flask.templating import render_template
from app.api_2_0.api import API2
from flask import request,session,redirect
"""
登陆模块
"""
@API2.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    pwd = request.form.get('password')
    from app.setting import USERNAME,PASSWORD
    if (username==USERNAME) and (pwd==PASSWORD):
        session['login'] = True
        return redirect('/index')
    return render_template('login.html',error='密码错误')

@login_required
@API2.route('/login/out',methods=['GET'])
def login_out():
    del session['login']
    return redirect('/login')