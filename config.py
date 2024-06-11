
SECRET_KEY = "asdsadfasfsfafsafsfdsaf"


#配置文件
from urllib.parse import quote
HOSTNAME='localhost'
password='wutong@871798'
port=3306
user='root'
database='exam_ceshi'
DB_URI = f"mysql+pymysql://{user}:{quote(password)}@{HOSTNAME}:{port}/{database}?charset=utf8"
SQLALCHEMY_DATABASE_URI=DB_URI



# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_USE_SSL=True  #是否加密
MAIL_PORT=465
MAIL_USERNAME='244894358@qq.com'
MAIL_PASSWORD='pzbfzxebkdfscaeg'
MAIL_DEFAULT_SENDER='244894358@qq.com'