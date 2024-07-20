from flask import (
    Flask, send_file, g, request, redirect, render_template, url_for
)
from werkzeug.utils import secure_filename
import os


def create_app():
    UPLOAD_FOLDER = '/uploads'

    app = Flask(__name__)


    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from . import db

    db.init_app(app)

    @app.route('/manifest.json')
    def serve_manifest():
        return send_file(
            'manifest.json',
            mimetype='application/manifest+json'
        )


    @app.route('/sw.js')
    def serve_sw():
        return send_file('sw.js', 'application/javascript')


    @app.route('/', methods=['GET', 'POST'])
    def index():
        if g.user is not None:
            return redirect(url_for('entry.entries'))
        if request.method == 'POST':
            return redirect(url_for('auth.login'))

        return render_template('index.html')


    from . import auth
    from . import entry
    from . import profile

    app.register_blueprint(auth.bp)
    app.register_blueprint(entry.bp)
    app.register_blueprint(profile.bp)

    return app


app = create_app() # para despliegue
