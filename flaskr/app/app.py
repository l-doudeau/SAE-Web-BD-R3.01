from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask import Flask
from secrets import token_urlsafe
from .models import * 
app = Flask(__name__)




#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://faucher:Thierry45.@servinfo-mariadb/DBfaucher'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/GRAND_GALOP'
app.config['SECRET_KEY'] = token_urlsafe(16) #Générer une clé au hasard
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.app_context().push()
