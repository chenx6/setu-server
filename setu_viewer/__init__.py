from flask import Flask


def create_app():
    from . import routes, models
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{app.instance_path}/url.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    routes.init_app(app)
    models.init_app(app)
    return app
