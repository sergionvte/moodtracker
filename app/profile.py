from flask import Blueprint, render_template
from .auth import login_required

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile/profile.html')
