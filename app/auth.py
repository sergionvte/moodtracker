import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']

        db, c = get_db()
        error = None

        c.execute(
            'SELECT id FROM users WHERE email = %s',
            (email,)
        )

        if not name:
            error = 'Name is required'

        if not email:
            error = 'Email is required'

        if not password:
            error = 'Password is required'

        if not age:
            error = 'Age is required'

        if c.fetchone() is not None: # podria ser elif
            error = 'User with email {} is already registered'.format(email)

        if error is None:
            c.execute(
                'INSERT INTO users (name, email, password, age) values (%s, %s, %s, %s)',
                (name, email, generate_password_hash(password), age)
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
