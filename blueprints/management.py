#管理相关
from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel
from .forms import RegisterForm,LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash

#（固定，固定，url前缀）
bp = Blueprint('management', __name__, url_prefix='/management')


#要访问下面的视图函数，路径为： /management/user
@bp.route('/user',methods=['GET','POST'])
def userManagement():
    return render_template('userManagement.html')


@bp.route("/question",methods=['GET','POST'])
def questionManagement():
    return render_template('questionManagement.html')