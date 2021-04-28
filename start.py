from flask import  session, g,redirect
from flask.helpers import url_for
from flask.templating import render_template
from app import create_app, db
from app.model import File, Share
app = create_app('default')
# 创建数据库
# db.create_all(app=app)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id
    g.download_user = None


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, File=File, Share=Share)


# @app.errorhandler(404)
# def error_view(error):
#     """
#     捕捉404
#     """
#     return render_template('404.html', error=error)
@app.route('/')
def index_():
    return redirect(url_for('web.index'))


@app.route('/favicon.ico')
def return_favicon():
    return app.send_static_file('favicon.ico')
if __name__ == "__main__":

    app.run(host='127.0.0.1',port=5000,debug=1)
