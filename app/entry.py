from flask import (
    Blueprint, render_template, request, redirect, url_for, g, flash
)
from werkzeug.exceptions import abort
from datetime import datetime
from .auth import login_required
from .db import get_db
import ast

bp = Blueprint('entry', __name__)

@bp.route('/entries', methods=['GET', 'POST'])
@login_required
def entries():
    db, c = get_db()
    c.execute(
        'SELECT e.id, e.emotion, e.description, e.created_at, e.modified_at, e.activities'
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
        selected_activities = request.form.get('selected_activities')

        if selected_activities is not None:
            selected_activities = ast.literal_eval(
                selected_activities
            )
            selected_activities = [
                element.replace('✖', '') for element in selected_activities
            ]
            activities_string = ';'.join(selected_activities)
        else:
            activities_string = ''



        error = None

        if not emotion:
            error = 'Emotion is required'

        if not description:
            error = 'Description is required'

        if error is None:
            db, c = get_db()
            c.execute(
                'INSERT INTO entries (emotion, description, created_by, created_at, modified_at, activities)'
                ' VALUES (%s, %s, %s, %s, %s, %s)',
                (emotion, description, g.user['id'], datetime.now(), datetime.now(), activities_string)
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
        emotion = request.form.get('selected_value')
        description = request.form.get('description')

        error = None

        if not emotion:
            error = 'Emotion is required.'

        if not description:
            error = 'Description is required.'

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
