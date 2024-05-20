from flask import (
    Blueprint, render_template, request, redirect, url_for, g, flash
)
from werkzeug.exceptions import abort
from datetime import datetime
from .auth import login_required
from .db import get_db

bp = Blueprint('entry', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('auth.login'))

    return render_template('index.html')


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    db, c = get_db()
    c.execute(
        'SELECT e.id, e.emotion, e.description, e.created_at, e.modified_at'
        ' FROM entries e JOIN users u ON e.created_by = u.id'
        ' WHERE e.created_by = %s ORDER BY modified_at DESC',
        (g.user['id'],)
    )
    entries = c.fetchall()

    return render_template('entry/dashboard.html', entries=entries)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        emotion = request.form['emotion']
        description = request.form['description']

        error = None

        if not emotion:
            error = 'Emotion is required'

        if not description:
            error = 'Description is required'

        if error is None:
            db, c = get_db()
            c.execute(
                'INSERT INTO entries (emotion, description, created_by, created_at, modified_at)'
                ' VALUES (%s, %s, %s, %s, %s)',
                (emotion, description, g.user['id'], datetime.now(), datetime.now())
            )
            db.commit()
            return redirect(url_for('entry.dashboard'))

        flash(error)
    
    return render_template('entry/create.html')


@bp.route('/update', methods=['GET', 'POST'])
def update():
    return render_template('entry/update.html')
