#授权相关
import random
import string

from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
from flask import request
import _string
from models import emailCaptchaModel
from .forms import RegisterForm,LoginForm
from models import userModel
from werkzeug.security import generate_password_hash,check_password_hash

#（固定，固定，url前缀）
bp = Blueprint('auth', __name__, url_prefix='/auth')


#要访问下面的视图函数，路径为： /auth/login
@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = userModel.query.filter_by(email=email).first()
            if not user:
                print("用户不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # cookie:
                # 1.cookie中不适合存储太多数据,只适合存放少量数据
                # 2.cookie一般用来存放登录或授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session["user_id"] = user.id
                return redirect("/")

            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))




        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# GET:从服务器上获取数据
# POST:将客户端的数据提交给服务器
@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == "GET":
    #验证用户提交的邮箱和验证码是否对应且正确
    # 表单验证：flask-wtf:wtforms
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)

        # 调用这个方法的时候，就会自动去调用类中的其他验证方法
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = userModel(email = email,username = username,password = generate_password_hash(password) )
            db.session.add(user)
            db.session.commit()
            return  redirect(url_for("auth.login"))

            # 2.验证码是否正确
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route('/mail/test')
def mail_test():
    message = Message(subject='邮箱测试',recipients=['3203809808@qq.com'],body='这是一条测试邮件')
    mail.send(message)
    return '邮件发送成功！'


# bp.route:如果没有指定methods参数，默认就是GET请求
@bp.route('/captcha/email')
def get_email_captcha():
    #传参1，路径传参：/captcha/email/<email>
    #传参2，：/captcha/email?email=xxx@qq.com
    email = request.args.get('email')
    #4/6:数字，数组；随机产生
    #string.digits:'1234567890'
    source = string.digits*4
    captcha = random.sample(source,4)
    print(captcha)
    captcha = ''.join(captcha)
    message = Message(subject='测试-注册验证码', recipients=[email], body=f'您的验证码是：{captcha}')
    mail.send(message)
    # 验证码可以缓存在memcached,redis缓存中
    # 用数据库存储
    email_captcha = emailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code:200/400/500,message:"",data:{}}
    return jsonify({'code':200,'message':'','data':None})
