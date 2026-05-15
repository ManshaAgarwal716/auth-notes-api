from fastapi import FastAPI
from .config import set
from src.db.main import init_db
from contextlib import asynccontextmanager
from src.users.routes import router 
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")
app=FastAPI(title="Notes API",version="1.0.0",lifespan=lifespan)
app.include_router(router,prefix="/api")