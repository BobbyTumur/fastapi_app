from fastapi import FastAPI
from tortoise import Tortoise

from config.database import init_db
from auth.auth_routes import router as auth_router



async def lifespan(app: FastAPI):
    # Initialize the database
    await init_db()
    yield
    # Close database connections
    await Tortoise.close_connections()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
    
