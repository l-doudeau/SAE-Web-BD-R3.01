from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secrets import token_urlsafe
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = token_urlsafe(16) #Générer une clé au hasard

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://faucher:Thierry45.@servinfo-mariadb/DBfaucher'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/DB'

db = SQLAlchemy(app)

app.app_context().push()



