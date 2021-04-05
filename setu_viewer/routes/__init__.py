from .nga import nga_bp
from .pixiv import pixiv_bp
from .api_v1 import api_bp
from .stage1st import s1_bp
from .adnmb import adnmb_bp

def init_app(app):
    app.register_blueprint(nga_bp)
    app.register_blueprint(pixiv_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(s1_bp)
    app.register_blueprint(adnmb_bp)
