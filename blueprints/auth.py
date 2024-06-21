#授权相关
import random
import string

from flask import Blueprint, jsonify
from exts import mail, db
from flask_mail import Message
from flask import request
from models import emailCaptchaModel
from models import userModel
from werkzeug.security import generate_password_hash, check_password_hash



#（固定，固定，url前缀）
# 创建蓝图对象，设置蓝图下的路由的前缀
bp = Blueprint('auth', __name__, url_prefix='/auth')


#要访问下面的视图函数，路径为： /auth/login
@bp.route('/login', methods=['POST'])
def login():
    # 获取 JSON 数据
    data = request.get_json()
    # print(data)
    # print(1)
    email = data.get('email')
    password = data.get('password')
    # print(email, password)

    # 检查邮箱和密码是否提供
    if not email or not password:
        return jsonify({'code': 400, 'message': '邮箱和密码不能为空'})

    # 验证用户
    user = userModel.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        # 用户不存在或密码错误
        return jsonify({'code': 400, 'message': '用户名或密码错误'})

    id = user.id
    username = user.username
    role = user.role

    # 返回成功响应
    return jsonify({'email': email, 'userId': id, 'userName': username, 'role': role, 'code': 200, 'message': '登录成功'})


@bp.route('/captcha/email', methods=['POST'])
def get_email_captcha():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'code': 400, 'message': '邮箱不能为空'}), 400

    # 生成验证码
    captcha = ''.join(random.sample(string.digits, 4))

    # 发送邮件
    message = Message(subject='注册验证码', recipients=[email], body=f'您的验证码是：{captcha}')
    mail.send(message)

    # 存储验证码到数据库
    email_captcha = emailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({'code': 200, 'message': '验证码发送成功'}), 200


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    captcha = data.get('captcha')
    userName = data.get('userName')

    # 检查邮箱、密码、验证码和用户名是否提供
    if not email or not password or not captcha or not userName:
        return jsonify({'code': 400, 'message': '邮箱、密码、验证码和用户名不能为空'}), 400

    # 验证验证码
    db_captcha = emailCaptchaModel.query.filter_by(email=email).first()
    print("前端：",captcha ,"后端",db_captcha.captcha)
    if not db_captcha or db_captcha.captcha != captcha:
        return jsonify({'code': 400, 'message': '验证码错误或已过期'}), 400

    # 验证用户是否已存在
    if userModel.query.filter_by(email=email).first():
        return jsonify({'code': 400, 'message': '邮箱已被注册'}), 400

        # 注册用户
    user = userModel(email=email, username=userName, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    recent_users = db.session.query(userModel).order_by(userModel.register_time.desc()).limit(1).all()
    latest_user = {"id": recent_users[0].id, "role": recent_users[0].role}
    print(latest_user)

    return jsonify({'code': 200, 'message': '注册成功', "latest_user": latest_user}), 200
