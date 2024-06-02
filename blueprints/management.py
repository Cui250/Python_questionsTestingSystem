#管理相关
from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
from flask import request
from models import emailCaptchaModel, choiceQuestionModel
from .forms import RegisterForm,LoginForm
from models import userModel
from werkzeug.security import generate_password_hash,check_password_hash
from decorators import login_required, admin_required

#（固定，固定，url前缀）
bp = Blueprint('management', __name__, url_prefix='/management')


#要访问下面的视图函数，路径为： /management/user
@bp.route('/user',methods=['GET','POST'])
def userManagement():
    return render_template('userManagement.html')


@bp.route("/question",methods=['GET','POST'])
# 检测用户是否登录
@login_required
# 检测用户身份是否为管理员
@admin_required
def questionManagement():
    if request.method == "GET":
        info = choiceQuestionModel.query.all()

        questions = []

        for i in info:
            question = {}
            options_str = i.option
            # 在视图函数中处理数据
            options_list = options_str.split('\n')
            question.update({'id': i.id})
            question.update({'question': i.question})
            question.update({'options': options_list})
            question.update({'answer': i.answer})
            questions.append(question)
            # 初始化session中的questions_management
            session["questions_management"] = questions
        # 将处理后的数据传递给模板
        return render_template('questionManagement.html',questions=questions)

    if request.method == "POST":
        if 'question' in request.form:
            question = request.form['question']
            option = request.form['option']
            answer = request.form['answer']
            choiceQuestion = choiceQuestionModel(question=question, option=option, answer=answer)
            db.session.add(choiceQuestion)
            db.session.commit()
        if 'question_id' in request.form:
            print(request.form['question_id'])
            question = choiceQuestionModel.query.get(int(request.form['question_id']))
            db.session.delete(question)
            db.session.commit()
            # 更新session中的questions_management
            session["questions_management"] = [item for item in session["questions_management"] if item['id'] != request.form['question_id']]
        return render_template('questionManagement.html',questions=session["questions_management"])
    return render_template('questionManagement.html')


