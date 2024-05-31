from flask import Flask, session,g,render_template
from sqlalchemy.testing.pickleable import User
from decorators import login_required

#导入配置文件
import config
from exts import db,mail
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.management import bp as management_bp
from blueprints.testing import bp as testing_bp
from flask_migrate import Migrate

app = Flask(__name__)
#绑定配置文件（自动读取）
app.config.from_object(config)

#将db对象进行绑定（先创建后绑定，防止循环引用）
db.init_app(app)
mail.init_app(app)
# ORM模型映射到数据库
migrate = Migrate(app, db)

#绑定蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(management_bp)
app.register_blueprint(testing_bp)


#blue print:用来做模块化的
#授权、管理、考试......每个模块定义为一个蓝图（blue print）

# flask db init:只需要执行一次
# flask db migrate:将ORM模型生成迁移脚本
# flask db upgrade:将迁移脚本映射到数据库中


# 钩子函数（正常流程中插入执行）：before_request / before_first_request / after_request
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        # g:用来存储全局变量的一个对象，需要导入才能使用
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


# 上下文处理器,实现了不用反复去数据库中取某个数据，所有页面在需要的时候直接来这里取（eg:登录的状态下一直显示用户名）
@app.context_processor
def my_context_processor():
    return {'user': g.user}


@app.route("/")
@login_required
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run()
