from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# declaring the db model (without initializing it)
db = SQLAlchemy()
login_manager=LoginManager() # declaring login_manager as an instance of LoginManager class from flask_login
bcrypt = Bcrypt() # declaring bcrypt to hash passwords in the database.


def create_app():
  app = Flask(__name__) #creating an app instance
  from app.config import Config
  app.config.from_object(Config) #initializing configurations from .config file
  login_manager.init_app(app) #initializing login_manager from flask lofgin
  db.init_app(app)  #initializing database model db with the flask app
  login_manager.login_view="login" # login.py will contain the code to authenticate the user and login
  bcrypt.init_app(app) #initializing bcrypt variable.




  
def load_user(user_id):
    from .models import User
    # Assuming you have a User model with a 'get' method that retrieves a user by their id
    return User.query.get(int(user_id))