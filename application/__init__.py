import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db, render_as_batch=True)

@app.before_first_request
def create_tables():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users_bp.login'


from application.core.views import core_bp
from application.users.views import users_bp
from application.appointments.views import appointments_bp
from application.profile.views import profile_bp
from application.medications.views import medications_bp
from application.oauth.views import oauth_bp

app.register_blueprint(core_bp)
app.register_blueprint(users_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(medications_bp)
app.register_blueprint(oauth_bp)
