from enum import Enum
from tortoise import fields
from tortoise.models import Model

from models.models import UserRole

class UserDatabase(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=31, unique=True)
    email = fields.CharField(max_length=63, unique=True)
    hashed_password = fields.CharField(max_length=127)
    role = fields.CharEnumField(UserRole)
    disabled = fields.BooleanField(default=False)

    class Meta:
        table = "users"
