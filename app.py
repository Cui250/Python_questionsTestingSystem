from flask import Flask
#导入配置文件
import config
from exts import db,mail
from models import userModel
from blueprints.auth import bp as auth_bp
from blueprints.testing import bp as testing_bp
from blueprints.paperSetting import bp as paperSetting_bp
from flask_migrate import Migrate
from blueprints.user_management import bp as user_management_bp
from blueprints.question_management import bp as question_management_bp

from flask_cors import CORS

app = Flask(__name__)

# 允许所有域名访问
CORS(app)
#绑定配置文件（自动读取）
app.config.from_object(config)
#将db对象进行绑定（先创建后绑定，防止循环引用）
db.init_app(app)
mail.init_app(app)
# ORM模型映射到数据库
migrate = Migrate(app, db)
#在主应用文件(app.py)中注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(testing_bp)
app.register_blueprint(paperSetting_bp)
app.register_blueprint(user_management_bp)
app.register_blueprint(question_management_bp)

#blue print:用来做模块化的
#授权、管理、考试......每个模块定义为一个蓝图（blue print）

# flask db init:只需要执行一次
# flask db migrate:将ORM模型生成迁移脚本
# flask db upgrade:将迁移脚本映射到数据库中

if __name__ == '__main__':
    app.run()
