from start import app
from flask_script import Manager
from flask_migrate import MigrateCommand
import os
from app.model import File,Share,db
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    db.create_all()

@manager.command
def init():
    os.system('python manager.py db init')

@manager.command
def migrate():
    os.system('python manager.py db migrate')

@manager.command
def upgrade():
    os.system('python manager.py db upgrade')

if __name__ == "__main__":
    manager.run()