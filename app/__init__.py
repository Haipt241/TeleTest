from flask import Flask

from extensions import db, cache, migrate
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import routes, models
        db.create_all()

    return app
