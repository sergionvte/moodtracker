from flask import Flask, send_file
import os


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

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

    from . import auth
    from . import entry

    app.register_blueprint(auth.bp)
    app.register_blueprint(entry.bp)

    return app


app = create_app() # para despliegue
