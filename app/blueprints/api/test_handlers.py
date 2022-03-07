from .blueprint import api
from app.base import db

@api.get("/test")
def Test():
    return "succeed!"


@api.get("/create_all")
def CreateAll():
    import app.models.model
    db.create_all()
    db.session.commit()
