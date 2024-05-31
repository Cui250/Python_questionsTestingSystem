#管理相关
from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel, ChoiceQuestionModel
from .forms import RegisterForm,LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash
from decorators import login_required
from decorators import login_required

#（固定，固定，url前缀）
bp = Blueprint('testing', __name__, url_prefix='/testing')




@bp.route('/',methods=['GET','POST'])
@login_required
def question():
    # 如果前端请求题目选项
    if request.method == 'GET':
        info = ChoiceQuestionModel.query.all()
        # 初始化session中的questions，如果它还不存在的话
        questions = []

        for i in info:
            question = {}
            options_str = i.option
            # 在视图函数中处理数据
            options_list = options_str.split('\n')
            question.update({'id' : i.id})
            question.update({'question':i.question})
            question.update({'options':options_list})
            question.update({'answer':i.answer})
            questions.append(question)

            session['questions'] = questions
        # 将处理后的数据传递给模板
        return render_template('testing.html', questions=questions)

    # 如果前端提交了答案，进行验证后返回结果
    if request.method == 'POST':
        questions = session['questions']
        # 拿到用户选择的所有答案
        answers = {}
        for answer in request.form:
            if answer.startswith('answer_'):
                question_id = int(answer.split('_')[1])
                answers[question_id] = request.form[answer]
        # 对每一题的答案进行判定后返回给前端，展示给用户
        results = {}
        # 把题目列表转换为一个大字典，并且把题目id作为大字典的键，
        # 其他信息依然是一个字典作为大字典的值，方便后面通过题目id来找题目答案
        questions_dict = {question['id']: question for question in questions}
        question_number = len(questions_dict)
        score_per_question = 100 / question_number
        count = 0
        for question_id,user_answer in answers.items():
            result = {}
            result['user_answer'] = user_answer
            result['correct_answer'] = questions_dict[question_id]['answer']
            if user_answer == questions_dict[question_id]['answer']:
                result['message'] = '哟哟哟~ 这你都答对了, 可真厉害呀~'
                count = count + 1
            else:
                result['message'] = '小菜鸡，答错了呢~'
            results[question_id] = result
        score = score_per_question * count
    #     将结果集返回前端
        return render_template('testing.html', questions=questions,results=results,score=score,question_number = question_number,count = count)


    return render_template('testing.html')


