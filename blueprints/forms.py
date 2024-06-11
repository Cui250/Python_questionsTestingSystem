import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import Email,Length,EqualTo,NumberRange
from models import  UserModel,EmailCaptchModel
# from exts import db
#用来验证前端提交i的数据是否符合要求
class RegisterForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致")])

    #自定义验证，邮箱是否用过
    def validate_email(self,filed):
        email=filed.data
        user=UserModel.query.filter_by(email=email).first()
        if user:
           raise wtforms.ValidationError(message="该邮箱已经被注册！")

    #自定义验证，验证码是否正确
    def validate_chaptcha(self, filed):
        captcha=filed.data
        email=self.email.data
        captcha_model=EmailCaptchModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或者验证码错误！")
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])


class DeleteUserForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])

class ChangeUserForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    identity = wtforms.StringField(validators=[Length(min=1, max=20, message="身份格式错误！")])

class DeleteQuestionForm(wtforms.Form):
    number = wtforms.IntegerField('Number',[NumberRange(min=1, max=999, message="题号格式错误！")])

class ChangeQuestionForm(wtforms.Form):
    number = wtforms.IntegerField('Number',[NumberRange(min=1, max=999, message="题号格式错误！")])
    question = wtforms.StringField(validators=[Length(min=1, max=200, message="问题格式错误！")])
    choice = wtforms.StringField(validators=[Length(min=1, max=200, message="选项格式错误！")])
    answer = wtforms.StringField(validators=[Length(min=1, max=1, message="答案格式错误！")])
    difficulty = wtforms.IntegerField('Number',[NumberRange(min=1, max=5, message="试题类别格式错误！")])
    kind = wtforms.StringField(validators=[Length(min=1, max=10, message="选项格式错误！")])
