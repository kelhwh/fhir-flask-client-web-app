import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'database.sqlite')

db = SQLAlchemy(app)
Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


from application.core.views import core
from application.users.views import users

app.register_blueprint(core)
app.register_blueprint(users)
