from flask import Blueprint
from app.base import app

from .api import blueprint as api_bp

if True:
    from .api import *


# 响应根路由健康检查请求
root = Blueprint("root", __name__)


@root.route("/", methods=["GET", "HEAD"])
def root_head_ping():
    return "ok"


# register blueprints
app.register_blueprint(root, url_prefix="/")
app.register_blueprint(api_bp._api, url_prefix="/api")