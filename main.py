import warnings
from fastapi import FastAPI

from config.database import init_db, close_db
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.admin_routes import router as admin_router



async def lifespan(app: FastAPI):
    # Initialize the database
    await init_db()
    yield
    # Terminate the database 
    await close_db()

warnings.filterwarnings("ignore", message=".*bcrypt*.", category=UserWarning)

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/api")
app.include_router(admin_router, prefix="/api")