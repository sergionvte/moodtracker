import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
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


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')

        db, c = get_db()
        error = None

        c.execute (
            'SELECT * FROM users WHERE email = %s', (email,)
        )

        user = c.fetchone()

        if user is None:
            error = 'User or password wrong'
        elif not check_password_hash(user['password'], password):
            error = 'User or password wrong'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            if remember:
                session.permanent = True
                current_app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = False

            return redirect(url_for('entry.dashboard'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/recovery', methods=['GET', 'POST'])
def recover_password():
    return render_template('auth/recover.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = c.fetchone()
        session.modified = True


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
