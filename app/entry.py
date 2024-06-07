from flask import (
    Blueprint, render_template, request, redirect, url_for, g, flash
)
import pytz
from werkzeug.exceptions import abort
from datetime import datetime
from .auth import login_required
from .db import get_db

bp = Blueprint('entry', __name__)

@bp.route('/entries', methods=['GET', 'POST'])
@login_required
def entries():
    db, c = get_db()
    c.execute(
        'SELECT e.id, e.emotion, e.description, e.created_at, e.modified_at'
        ' FROM entries e JOIN users u ON e.created_by = u.id'
        ' WHERE e.created_by = %s ORDER BY modified_at DESC',
        (g.user['id'],)
    )
    entries = c.fetchall()

    return render_template('entry/entries.html', entries=entries)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        emotion = request.form['selected_value']
        description = request.form['description']

        error = None

        if not emotion:
            error = 'Emotion is required'

        if not description:
            error = 'Description is required'

        if error is None:
            db, c = get_db()
            current_datetime = datetime.now()
            user_timezone = request.headers.get('Timezone')  # Get the user's timezone from the request headers
            user_datetime = current_datetime.astimezone(pytz.timezone(user_timezone))  # Convert the datetime to the user's timezone
            c.execute(
                'INSERT INTO entries (emotion, description, created_by, created_at, modified_at)'
                ' VALUES (%s, %s, %s, %s, %s)',
                (emotion, description, g.user['id'], user_datetime, user_datetime)
            )
            db.commit()
            return redirect(url_for('entry.entries'))

        flash(error)

    return render_template('entry/create.html')


def get_entry(id):
    db, c = get_db()

    c.execute(
    'SELECT e.id, e.emotion, e.description, e.created_by, e.created_at, e.modified_at'
    ' FROM entries e JOIN users u ON e.created_by = u.id WHERE e.id = %s',
    (id,)
)
    entry = c.fetchone()

    if entry is None:
        abort(404, 'This entry {} does not exist'.format(id))

    return entry


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    entry = get_entry(id)

    if request.method == 'POST':
        emotion = request.form['emotion']
        description = request.form['description']

        error = None

        if not emotion:
            error = 'Emotion is required'

        if not description:
            error = 'Description is required'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'UPDATE entries SET emotion = %s, description = %s, modified_at = %s'
                ' WHERE id = %s AND created_by = %s',
                (emotion, description, datetime.now(), id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('entry.entries'))
    return render_template('entry/update.html', entry=entry)

@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'DELETE FROM entries'
        ' WHERE id = %s AND created_by = %s',
        (id, g.user['id'])
    )
    db.commit()
    return redirect(url_for('entry.entries'))
