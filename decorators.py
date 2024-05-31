from functools import wraps
from flask import g,redirect,url_for
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


    return inner