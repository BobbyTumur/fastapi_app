from config.settings import settings
from tortoise import Tortoise

DATABASE_CONFIG = {
    "connections": {
        "default": settings.database_url,
    },
    "apps": {
        "models": {
            "models": ["models.db_models"],
            "default_connection": "default",
        }
    }
}

async def init_db():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()