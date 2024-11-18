from flask import Blueprint, redirect, url_for, render_template
from .models import db, User

delete_user_bp = Blueprint('delete_user', __name__)

@delete_user_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('login.login'))
    return render_template('profile.html', user_id=user_id)