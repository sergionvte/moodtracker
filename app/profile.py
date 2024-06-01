from flask import Blueprint, render_template

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile/profile.html')

