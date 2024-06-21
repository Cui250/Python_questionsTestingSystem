from exts import db
from datetime import datetime
from sqlalchemy import JSON

class userModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),unique = True,nullable=False)
    role = db.Column(db.String(100),nullable=True ,default='student')
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
    answer = db.Column(db.String(200), nullable=True)
    analysis = db.Column(db.String(200), nullable=True, default="略")
    course = db.Column(db.String(200), nullable=True)
    knowledge_point = db.Column(db.String(200), nullable=True)
    level = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(2), nullable=True)

class testPaperModel(db.Model):
    __tablename__ = 'test_paper'
    paper_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.String(200), nullable=True)
    score_per_question = db.Column(JSON, nullable=True)


class testingResultModel(db.Model):
    __tablename__ = 'test_result'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paper_id = db.Column(db.Integer, db.ForeignKey('test_paper.paper_id'), nullable=False)
    score = db.Column(db.Numeric(5, 2), nullable=False)
    answer_situation = db.Column(JSON, nullable=True)
    testingTime = db.Column(db.DateTime, default=datetime.now())
























