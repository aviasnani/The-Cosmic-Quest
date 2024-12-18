from flask import Blueprint, redirect, url_for
from flask_login import logout_user, login_required

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login.login'))