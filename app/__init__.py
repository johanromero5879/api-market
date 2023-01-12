from dotenv import load_dotenv
from fastapi import FastAPI

# Import routes

# App setup
load_dotenv()
app = FastAPI()

# Config routes


@app.get("/")
async def root():
    return "Welcome to api market, made in FastAPI"

