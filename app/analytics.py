import base64
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg') # This needs to happen before any pyplot import!!!

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from werkzeug.exceptions import abort
from datetime import datetime
from .auth import login_required
from .db import get_db
from io import BytesIO
from matplotlib.figure import Figure
from flask import (
    Blueprint, render_template, request, redirect, url_for, g, flash
)

bp = Blueprint('analytics', __name__)

sns.set_theme()

@bp.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    db, c = get_db()
    c.execute(
        'SELECT e.id, e.emotion, e.description, e.created_at, e.modified_at'
        ' FROM entries e JOIN users u ON e.created_by = u.id'
        ' WHERE e.created_by = %s ORDER BY modified_at DESC',
        (g.user['id'],)
    )

    print(g.user['id'])
    entries = c.fetchall()
    print(get_emotions(entries))
    print(len(get_emotions(entries)))

    # graphics area
    data = get_emotions(entries)
    emotion_counts = data['emotion'].value_counts()

    fig = Figure()
    ax = fig.subplots()
    ax.barh(emotion_counts.index, emotion_counts.values)

    ax.set_xlabel('Amount')
    ax.set_ylabel('Emotion')
    ax.set_title('Summary')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    #end graphics area

    return render_template('analytics/analytics.html', entries=get_emotions(entries), data=data)


def get_emotions(entries):
    return pd.DataFrame(entries)
