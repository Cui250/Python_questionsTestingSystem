from flask import Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchModel
from .forms import  RegisterForm,LoginForm,DeleteUserForm,ChangeUserForm
from models import UserModel
from werkzeug.security import generate_password_hash,check_password_hash
#auth的蓝图，用来写视图
bp=Blueprint("auth", __name__,url_prefix="/auth")



@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@bp.route("/guanliyuan")
def guanliyuan():
    return render_template("guanliyuan.html")

@bp.route('/lookuser')
def look_user():
    users = UserModel.query.all()
    return render_template("lookuser.html",users=users)

@bp.route("/deleteuser",methods=["GET","POST"])
def delete_user():
    if request.method == 'GET':
       return render_template("deleteuser.html")
    else:
        form = DeleteUserForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            user = UserModel.query.filter_by(email=email).first()
            if user.username == username:
                db.session.delete(user)
                db.session.commit()
                return "删除成功"
            else:
                return "邮箱或用户名错误--删除失败"
        else:
            return "邮箱或用户名错误--删除失败"

@bp.route("/changeuser",methods=["GET","POST"])
def change_user():
    if request.method == 'GET':
       return render_template("changeuser.html")
    else:
        form =ChangeUserForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            identity = form.identity.data
            if  identity not in ('学生', '老师', '管理员'):
                return "你的修改不符合规范--修改失败"
            else:
                if not UserModel.query.filter_by(email=email).first() :
                    user = UserModel(email=email, username=username, password=generate_password_hash(password),identity=identity)
                    db.session.add(user)
                    db.session.commit()
                else:
                    user = UserModel.query.filter_by(email=email).first()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.identity = identity
                    db.session.commit()
                return "数据修改成功"
        else:
            return "你的修改不符合规范--修改失败"


@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method=='GET':
       return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print('邮箱不存在！')
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,password):
                session['user_id'] = user.id
                #cookie:
                #cookie中不适合存储大量数据
                #cookie一般用来存储登录授权的东西
                #flask中的session,是经过加密后存储在cookie中的
                if user.identity=='管理员':
                    return redirect(url_for("auth.guanliyuan"))
                if user.identity=="学生":
                    return "你是一个学生"
                else:
                    return "你是一个老师"

            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("auth.login"))
# 如果没有指定methods参数，默认是GET请求
# GET:从服务器获取数据
# POST:将客户端的数据提交给服务器
@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
         # 验证信息是否符合注册要求
         # 表单验证：flask-wtf
         form=RegisterForm(request.form)
         if form.validate():
             email=form.email.data
             username=form.username.data
             password=form.password.data
             user=UserModel(email=email,username=username,password=generate_password_hash(password),identity='学生')
             db.session.add(user)
             db.session.commit()
             return redirect(url_for("auth.login"))
         else:
             print(form.errors)
             return redirect(url_for("auth.register"))


@bp.route("/captcha/email")
def get_captcha_email():
    #/captcha/email/<emial>
    #/captcha/email?emial=xxxx
    email=request.args.get("email")
    sours=string.digits*4
    captcha=random.sample(sours,4)
    captcha="".join(captcha)
    message = Message(subject="测试系统验证码",recipients=[email],body=f"您的验证码是:{captcha}")
    mail.send(message)
    #/memcached/redis
    #用数据库存储
    email_captcha=EmailCaptchModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code:200/400/500,message:"",data:{}}
    return jsonify({"code": 200, "message": "", "data": None})




@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试",recipients=["1480289352@qq.com"],body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"