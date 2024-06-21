from flask import Blueprint,jsonify,make_response
from exts import db
from flask import request
from models import userModel
from werkzeug.security import generate_password_hash
#auth的蓝图，用来写视图
bp=Blueprint("user_management", __name__,url_prefix="/user_management")


# 渲染题目到前端,对应load_user
@bp.route("/returnusers", methods=['GET'])
def returnusers():
    try:
        users = userModel.query.all()
        responseBody = {
            'data': [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'register_time': user.register_time,

    } for user in users]
        }
        return make_response(jsonify(responseBody)), 200
    except Exception as e:
        # 这里可以根据需要记录日志
        return make_response(jsonify({'error': 'An error occurred', 'message': str(e)})), 500

# 重置密码接口
@bp.route("/changepassword", methods=['POST'])
def change_password():
    response_object = {'status': 'fail', 'message': ''}
    if request.method == 'POST':
        post_data = request.get_json()
        email = post_data.get('data', {}).get('email')
        password = post_data.get('data', {}).get('password')
        user = userModel.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(password)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = '重置密码成功!'
            return jsonify(response_object) # 明确返回200状态码
        else:
            response_object['message'] = '重置失败，用户不存在!'
            return jsonify(response_object), 404  # 用户不存在，返回404状态码
    else:
        response_object['message'] = '请求方法不正确'
        return jsonify(response_object), 405  # 请求方法不正确，返回405状态码

# 用来处理个人信息页面的重置密码操作，因为post传回的数据格式不同，所以新建了个视图函数
@bp.route("/changepassword_new", methods=['POST'])
def change_password_new():
    response_object = {'status': 'fail', 'message': ''}
    if request.method == 'POST':
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        user = userModel.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(password)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = '重置密码成功!'
            return jsonify(response_object) # 明确返回200状态码
        else:
            response_object['message'] = '重置失败，用户不存在!'
            return jsonify(response_object), 404  # 用户不存在，返回404状态码
    else:
        response_object['message'] = '请求方法不正确'
        return jsonify(response_object), 405  # 请求方法不正确，返回405状态码

# 删除用户接口
@bp.route("/deleteuser", methods=['DELETE'])
def deleteuser():
    response_object = {'status': 'fail', 'message': ''}
    if request.method == 'DELETE':
        post_data = request.get_json()
        print('调用删除试题方传过来的参数是：', post_data)
        id = post_data.get('id')
        user = userModel.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)  # 修正：使用 delete()
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = '删除成功!'
        else:
            response_object['message'] = '删除失败，用户不存在!'
    else:
        response_object['message'] = '请求方法不正确'
    return jsonify(response_object)  # 确保返回 JSON 响应

#
# 编辑用户接口
@bp.route("/changeuser",methods=['POST'])
def changeuser():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用编辑用户方法传过来的参数是：', post_data)
        id = post_data.get('id')
        username = post_data.get('username')
        email = post_data.get('email')
        role = post_data.get('role')
        if role not in ('admin', 'student', 'teacher'):
            response_object['message'] = '用户身份格式错误，身份只能是teacher，student或admin!'
            response_object["status"] = 'fail'
            return response_object
        else:
            user = userModel.query.filter_by(id=id).first()
            if user:
                user.username = username
                user.email = email
                user.role = role
                db.session.commit()
                response_object['message'] = '修改用户成功!'
                response_object["status"] = 'success'
                return response_object
            else:
                response_object['message'] = '用户不存在，修改失败!'
                response_object["status"] = 'success'
                return response_object


#增添用户接口
@bp.route("/adduser",methods=['POST'])
def adduser():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print('调用增添用户方法传过来的参数是：', post_data)
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        role = post_data.get('role')
        if role not in ('admin', 'student', 'teacher'):
            response_object['message'] = '用户身份格式错误，身份只能是teacher，student或admin!'
            response_object["status"] = 'fail'
            return response_object
        else:
            user = userModel(username=username, email=email, password=generate_password_hash(password),
                                     role=role)
            db.session.add(user)
            db.session.commit()
            response_object['message'] = '添加成功!'
            response_object["status"] = 'success'
            return response_object
