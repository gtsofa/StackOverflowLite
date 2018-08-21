from flask import Flask

from config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Register the question blueprint
    from app.api.v1.questions import question as question_blueprint
    app.register_blueprint(question_blueprint, url_prefix='/api/v1')

    return app