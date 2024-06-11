from flask import Flask,session,g
import config
from exts import db,mail
from models import UserModel
from flask_migrate import Migrate
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp  as auth_bp

app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
#blueprint:用来模块化

#before_request/before_first_request/agter_request///钩子函数
#hook
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id  :
        user = UserModel.query.get(user_id)
        setattr(g,'user',user)
    else:
        setattr(g, 'user', None)

@app.context_processor
def my_context_processor():
    return {'user':g.user}


if __name__ == '__main__':
    app.run()
