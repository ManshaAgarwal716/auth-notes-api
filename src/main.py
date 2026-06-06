from fastapi import FastAPI
from .config import set
from src.db.main import init_db
from contextlib import asynccontextmanager
from src.users.routes import router 
from src.notes.routes import note
from src.middleware import register_middleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")
app=FastAPI(title="Notes API",version="1.0.0",lifespan=lifespan)
register_middleware(app)
app.include_router(router,prefix="/api")
app.include_router(note)