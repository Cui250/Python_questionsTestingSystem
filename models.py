from exts import db
from datetime import datetime
class userModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),unique = True,nullable=False)
    role = db.Column(db.String(100),nullable=True)
    register_time = db.Column(db.DateTime,default=datetime.now)

class emailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    # used = db.Column(db.Boolean, default=False)


class choiceQuestionModel(db.Model):
    __tablename__ = 'choicequestion'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    question = db.Column(db.String(200), nullable=True)
    option = db.Column(db.String(200), nullable=True)
    answer = db.Column(db.String(10), nullable=True)
    analysis = db.Column(db.String(200), nullable=True)
    course = db.Column(db.String(200), nullable=True)
    knowledge_point = db.Column(db.String(200), nullable=True)
    level = db.Column(db.String(200), nullable=True)

class testPaperModel(db.Model):
    __tablename__ = 'test_paper'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course = db.Column(db.String(200), nullable=False)

class paperQuestionModel(db.Model):
    __tablename__ = 'paper_question'
    # 外键
    paper_id = db.Column(db.Integer, db.ForeignKey('test_paper.id'), primary_key=True)
    question_id = db.Column(db.Integer,  db.ForeignKey('choicequestion.id'), primary_key=True)























