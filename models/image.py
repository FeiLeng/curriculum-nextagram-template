from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Photos(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='images', null=False)
    images = pw.CharField(unique=False)

