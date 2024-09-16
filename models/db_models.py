from tortoise import fields
from tortoise.models import Model
from enum import Enum

class UserRole(Enum):
    TIER1 = "Tier1"
    TIER2 = "Tier2"
class UserInDB(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=31, unique=True)
    email = fields.CharField(max_length=63, unique=True)
    hashed_password = fields.CharField(max_length=127)
    role = fields.CharEnumField(UserRole, default=UserRole.TIER1)
    disabled = fields.BooleanField(default=False)

    class Meta:
        table = "users"
