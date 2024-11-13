from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .__init__ import db

db=SQLAlchemy()

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  fname = db.Column(db.String(20), nullable = False)
  lname = db.Column(db.String(20), nullable = False)
  email = db.Column(db.String(40), nullable = False, unique=True)
  phone = db.Column(db.String(20), nullable = False, unique=True)
  username = db.Column(db.String(20), nullable = False, unique = True)
  password = db.Column(db.String(100), nullable = False)

class Score(db.Model):
  score_id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  score = db.Column(db.Integer, nullable=False)

  