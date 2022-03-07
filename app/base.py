from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import app.config as config

app = Flask(__name__)

for key in dir(config):
    if key not in [
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__spec__",
    ]:
        app.config[key] = getattr(config, key)

def create_sqlalchemy_app():
    from sqlalchemy.dialects import mysql as mysql_types

    _db = SQLAlchemy(app)
    print("create_sqlalchemy_app")
    # 为了触发after_transaction_create hook
    _db.session.commit()

    # 补充缺失的 mysql 专用类型，以配合类型劫持系统的使用
    _db.LONGTEXT = mysql_types.LONGTEXT
    _db.BIGINT = mysql_types.BIGINT
    _db.INTEGER = mysql_types.INTEGER
    _db.TINYINT = mysql_types.TINYINT
    return _db

db = create_sqlalchemy_app()
print("db ready")

redis = Redis.from_url(
    config.REDIS_URL,
    decode_responses=True,
    encoding="utf-8",
    max_connections=app.config.get("REDIS_MAX_CONNECTIONS") or 500,
    socket_timeout=5,
    socket_connect_timeout=5,
)

print("redis ready")