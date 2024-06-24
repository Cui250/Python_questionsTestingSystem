#数据库的配置信息(改成你自己的)
hostname = '127.0.0.1'
port = '3306'
username = 'root'
password = 'ABSESP040113'
database = 'questions'
# （不要有空格！！！）：
DB_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}'
SQLALCHEMY_DATABASE_URI = DB_URI



# DB_URI = f"mysql://{username}:{password}@{hostname}/{database}"
# SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱smtp配置信息
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
# 下面也是改成你的邮箱配置信息：用户名（邮箱地址），生成的授权码，默认发送邮箱（也是邮箱地址）
MAIL_USERNAME = ' '
MAIL_PASSWORD = ' '
MAIL_DEFAULT_SENDER = ' '
