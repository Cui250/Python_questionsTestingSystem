#创建模型
from exts import db
from datetime import datetime

#flask db init
#flask db migrate
#flask db upgrade
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)
    identity = db.Column(db.String(20),nullable=False)


class EmailCaptchModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)

class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    question = db.Column(db.String(200), nullable=False)
    choice = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(10), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.String(10), nullable=False)