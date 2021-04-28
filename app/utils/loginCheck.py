from flask import request,session
from functools import wraps

from werkzeug.utils import redirect

def login_required(f):
    @wraps(f)
    def inner(*args,**kwargs):
        try:
            if not session['login']:
                return redirect('/login')
            return f(*args,**kwargs)
        except KeyError:
            session['login'] = False
            return redirect('/login')
    return inner