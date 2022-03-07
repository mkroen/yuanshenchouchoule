from sqlalchemy import text
from app.base import db


class BaseModel:
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp(), comment="创建时间")
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="更新时间",
    )
    deleted = db.Column(db.Boolean, default=False, comment="是否删除,软删除标记")