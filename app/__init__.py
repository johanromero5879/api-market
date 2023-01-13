from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import routes
from app.user.infrastructure.rest import user_routes

# App setup
load_dotenv()
app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Config routes
app.include_router(user_routes.router)


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/pages/api.html")

