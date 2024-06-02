from functools import wraps
from flask import g,redirect,url_for
# 创建装饰器，确保用户已经登录才能进行后续操作
def login_required(func):
    #保留func的信息
    @wraps(func)
    # *args:1,2,3，...
    # ** kwargs:乱序的关键词参数
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))


    return  inner


def admin_required(func):
    #保留func的信息
    @wraps(func)
    # *args:1,2,3，...
    # ** kwargs:乱序的关键词参数
    def inner(*args, **kwargs):
        if g.user.role == 'admin':
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))


    return inner