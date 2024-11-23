from flask import Blueprint, redirect, url_for, render_template
from .models import db, User
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from .__init__ import bcrypt

confirm_delete_bp = Blueprint('confirm_delete',__name__)

class ConfirmDelete(FlaskForm):
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
   submit = SubmitField("Delete Account")
  
@confirm_delete_bp.route('/confirm_delete/<int:user_id>', methods=["GET", "POST"])
def confirm_delete(user_id):
  form=ConfirmDelete()
  user=User.query.get(user_id)
  error = None
  if form.validate_on_submit():
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      db.session.delete(user)
      db.session.commit()
      return redirect(url_for('login.login'))
    else:
      error = "Incorrect password, Enter the correct password to delete your account."
  return render_template('confirm_delete.html', user_id=user_id, form=form, error=error)


   
  


'''user = User.query.get(user_id)
    form = LoginForm()
    if user:
        if form.username
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('login.login'))
    return render_template('profile.html', user_id=user_id)'''