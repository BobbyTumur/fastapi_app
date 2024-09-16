from config.enviroment import env
from tortoise import Tortoise

DATABASE_CONFIG = {
    "connections": {
        "default": env.database_url,
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

async def close_db():
    await Tortoise.close_connections()