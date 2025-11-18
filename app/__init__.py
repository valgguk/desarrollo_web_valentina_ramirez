# app/__init__.py
from flask import Flask
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        # db.create_all()  # NO en producción; usar solo si BD vacía y coincide con schema
        pass

    from .routes import bp
    app.register_blueprint(bp)

    return app