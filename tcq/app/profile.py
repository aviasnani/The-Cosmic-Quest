from flask import Blueprint, render_template
from flask_login import login_required, current_user

profile_bp = Blueprint('profile', __name__)



@profile_bp.route('/profile', methods=["GET","POST"])
@login_required
def profile():
  first_name = current_user.fname
  last_name = current_user.lname
  email = current_user.email
  phone = current_user.phone
  username = current_user.username
  user_id=current_user.id
  return render_template('profile.html', first_name = first_name, last_name = last_name, email = email, phone = phone, username=username, user_id=user_id)