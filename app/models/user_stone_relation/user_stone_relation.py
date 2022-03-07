from app.base import db
from app.helpers.database.base_model import BaseModel

class UserStoneRelation(BaseModel):
    user_id = db.Column(db.BIGINT, comment="user.id")
    stone = db.Column(db.INTEGER, comment="原石数")