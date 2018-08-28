from flask import Flask

from app.config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # Register the auth blueprint
    from app.api.v1.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    # Register the question blueprint
    from app.api.v1.questions import question as question_blueprint
    app.register_blueprint(question_blueprint, url_prefix='/api/v1')

    # Register the auth_v2 blueprint
    from app.api.v2.auth import auth_v2 as auth_v2_blueprint
    app.register_blueprint(auth_v2_blueprint, url_prefix='/api/v2/auth')

    # Register the question_v2 blueprint
    from app.api.v2.questions import question_v2 as question_v2_blueprint
    app.register_blueprint(question_v2_blueprint, url_prefix='/api/v2')

    return app