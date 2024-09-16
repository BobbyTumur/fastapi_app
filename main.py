from fastapi import FastAPI

from config.database import init_db, close_db
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.admin_routes import router as admin_router



async def lifespan(app: FastAPI):
    # Initialize the database
    await init_db()
    yield
    # Close database connections
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(admin_router, prefix="/admin")