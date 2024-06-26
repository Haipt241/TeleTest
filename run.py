import logging

from flask import Flask

from gevent.pywsgi import WSGIServer
from extensions import cache
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cache.init_app(app)

    with app.app_context():
        from app.routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app


app = create_app()

if __name__ == "__main__":
    port = 5002
    http_server = WSGIServer(('0.0.0.0', port), app)
    logger.info(f"Starting server on port {port}")
    http_server.serve_forever()
