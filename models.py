from exts import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),unique = True,nullable=False)
    role = db.Column(db.String(100),nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    # used = db.Column(db.Boolean, default=False)


class ChoiceQuestionModel(db.Model):
    __tablename__ = 'choicequestion'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    question = db.Column(db.String(200), nullable=False)
    option = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(10), nullable=False)
    analysis = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(200), nullable=False)
    knowledge_point = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(200), nullable=False)





















