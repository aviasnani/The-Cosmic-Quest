from flask import Blueprint, redirect, render_template, url_for, session
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from models import User
from __init__ import bcrypt

login_bp = Blueprint('login', __name__)

class LoginForm(FlaskForm):
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
  password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Login")

@login_bp.route('login', methods=['GET', 'POST'])
def login():
  error = None
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      if bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user) 
        session.pop('score', None)  # clearning the score session variable
        session.pop('message', None) # clearing the message session variable
        return redirect(url_for('dashboard'))
      else:
       error = "Incorrect Password!"
    else: 
      error = "Username not found!"
  return render_template('login.html',form=form, error=error)
