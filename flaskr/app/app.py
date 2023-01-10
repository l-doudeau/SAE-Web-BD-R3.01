from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask import Flask
from secrets import token_urlsafe
from .models import * 
from flask_mail import Mail, Message
app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "thelendpvp@gmail.com",
    "MAIL_PASSWORD": "yqfjxbfahjqgqthz"}

app.config.update(mail_settings)
mail = Mail(app)
app.config['SECRET_KEY'] = token_urlsafe(16) #Générer une clé au hasard

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://faucher:Thierry45.@servinfo-mariadb/DBfaucher'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://doudeau:doudeau@servinfo-mariadb/DBdoudeau'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/GRAND_GALOP'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://doudeau:doudeau@localhost/GRAND_GALOP'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.app_context().push()
