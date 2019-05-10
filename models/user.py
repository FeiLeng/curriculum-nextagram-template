from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    profilepic = pw.CharField(unique=False, null=True)


def is_authenticated():
    return True
