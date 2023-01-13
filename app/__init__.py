from dotenv import load_dotenv
from fastapi import FastAPI

# Import routes
from app.user.infrastructure.rest import user_routes

# App setup
load_dotenv()
app = FastAPI()

# Config routes
app.include_router(user_routes.router)


@app.get("/")
async def root():
    return "Welcome to api market, made in FastAPI"

