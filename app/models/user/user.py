from app.base import db
from app.helpers.database.base_model import BaseModel

class User(BaseModel):
    mobile = db.Column(db.String(64), comment="手机号")
    wx_open_id = db.Column(db.String(64), comment="wx_open_id")
    gender = db.Column(db.String(64), comment="性别 0:未知 1:男 2:女")
    description = db.Column(db.String(64), comment="描述")
    avatar = db.Column(db.String(256), comment="头像")
    address = db.Column(db.String(128), comment="地址")
    