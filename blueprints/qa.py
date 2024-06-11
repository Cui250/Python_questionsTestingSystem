from flask import Blueprint,request,render_template,g,redirect,url_for
from models import QuestionModel
from exts import db
from .forms import  DeleteQuestionForm,ChangeQuestionForm
import string
#qa的蓝图，用来写视图
bp = Blueprint('qa', __name__, url_prefix='/qa')

@bp.route('/lookquestion')
def look_question():
    questions = QuestionModel.query.all()
    return render_template("lookquestion.html", questions=questions)

@bp.route("/deletequestion",methods=["GET","POST"])
def delete_question():
    if request.method == 'GET':
       return render_template("deletequestion.html")
    else:
        form = DeleteQuestionForm(request.form)
        if form.validate():
            id=form.number.data
            Question = QuestionModel.query.filter_by(id=id).first()
            if Question:
                db.session.delete(Question)
                db.session.commit()
                return "删除成功"
            else:
                return "题号不存在--删除失败"
        else:
            return "--删除失败"

@bp.route("/changequestion",methods=["GET","POST"])
def change_question():
    if request.method == 'GET':
       return render_template("changequestion.html")
    else:
        form =ChangeQuestionForm(request.form)
        if form.validate():
            id=form.number.data
            question=form.question.data
            choice=form.choice.data
            answer=form.answer.data
            difficulty=form.difficulty.data
            kind=form.kind.data
            if  answer not in ('A', 'B', 'C','D'):
                return "你的修改不符合规范--修改失败"
            else:
                if not QuestionModel.query.filter_by(id=id).first() :
                    Question = QuestionModel(id=id, question=question,choice=choice,answer=answer, difficulty=difficulty, kind=kind)
                    db.session.add(Question)
                    db.session.commit()
                else:
                    Question = QuestionModel.query.filter_by(id=id).first()
                    Question.question = question
                    Question.choice = choice
                    Question.answer = answer
                    Question.difficulty = difficulty
                    Question.kind = kind
                    db.session.commit()
                return "数据修改成功"
        else:
            return "你的修改不符合规范--修改失败"