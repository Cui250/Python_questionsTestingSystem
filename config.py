#数据库的配置信息
hostname = '127.0.0.1'
port = '3306'
username = 'root'
password = 'ABSESP040113'
database = 'questions'
# 固定写法（不要有空格！！！）：
DB_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}'
SQLALCHEMY_DATABASE_URI = DB_URI



# DB_URI = f"mysql://{username}:{password}@{hostname}/{database}"
# SQLALCHEMY_DATABASE_URI = DB_URI


# dlujicapiwfndfgd
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '2686036382@qq.com'
MAIL_PASSWORD = 'dlujicapiwfndfgd'
MAIL_DEFAULT_SENDER = '2686036382@qq.com'

# 用于哈希加密存储的密码的秘钥
SECRET_KEY = 'ABC123'


