from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from .models import * 
app = Flask(__name__)




app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://faucher:Thierry45.@servinfo-mariadb/DBfaucher'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://doudeau:doudeau@localhost/GRAND_GALOP'

db = SQLAlchemy(app)

app.app_context().push()
