from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from .models import db


login_manager=LoginManager() # declaring login_manager as an instance of LoginManager class from flask_login
bcrypt = Bcrypt() # declaring bcrypt to hash passwords in the database.


def create_app():
  app = Flask(__name__) #creating an app instance
  from app.config import Config
  app.config.from_object(Config) #initializing configurations from .config file
  print(f"Database URI: {os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'][9:])}")
  login_manager.init_app(app) #initializing login_manager from flask lofgin
  db.init_app(app)  #initializing database model db with the flask app
  login_manager.user_loader(load_user)
  login_manager.login_view="login" # login.py will contain the code to authenticate the user and login
  bcrypt.init_app(app) #initializing bcrypt variable.
  #importing blueprint from their respective files for initializing them
  from .home import home_bp
  from .dashboard import dashboard_bp
  from .login import login_bp
  from .signup import signup_bp
  from .profile import profile_bp
  from .logout import logout_bp
  from .delete_user import confirm_delete_bp
  #initializing blueprints
  app.register_blueprint(confirm_delete_bp)
  app.register_blueprint(logout_bp)
  app.register_blueprint(profile_bp)
  app.register_blueprint(login_bp)
  app.register_blueprint(signup_bp)
  app.register_blueprint(dashboard_bp)
  app.register_blueprint(home_bp)
  return app




  
def load_user(user_id):
    from .models import User
    # Assuming you have a User model with a 'get' method that retrieves a user by their id
    return User.query.get(int(user_id))