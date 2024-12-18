from flask import Blueprint, render_template, redirect, url_for
from .models import User, Score, db
from .__init__ import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, ValidationError, Length
from flask_sqlalchemy import SQLAlchemy

signup_bp=Blueprint('signup', __name__)

class SignupForm(FlaskForm):
  fname = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "First Name"})
  lname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name"})
  email = EmailField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Email id"})
  phone = StringField(validators=[InputRequired(), Length(min=10, max=20)], render_kw={"placeholder": "Phone number"})
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
  password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
  confirm_password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Confirm Password"})
  submit = SubmitField("Signup")
  #error = ""
  def validate_username(self, username):
    existing_username = User.query.filter_by(username=username.data).first()
    if existing_username:
      raise ValidationError("This username already exists, Try another one.")
  def validate_email(self, email):
    existing_email = User.query.filter_by(email=email.data).first()
    if existing_email:
      raise ValidationError("This email id already exists.")
  def validate_phone(self, phone):
    existing_phone = User.query.filter_by(phone=phone.data).first()
    if existing_phone:
      raise ValidationError("This phone number already exists.")
  


@signup_bp.route('/signup', methods=["GET", "POST"])
def signup():
  form=SignupForm()
  error = None
  if form.validate_on_submit():
      if form.confirm_password.data == form.password.data:
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, phone=form.phone.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user) #adding new user to the database
        db.session.commit()
        initial_score = Score(user_id=new_user.id, score=0) #setting an initial score of 0 for every new user
        db.session.add(initial_score) # adding that initial score to the score table in the database
        db.session.commit() #saving changes
        return redirect(url_for('login.login')) #redirecting to login after the new user is created
      else:
        error = "Passwords do not match"

    
  return render_template('signup.html',form=form, error=error)

