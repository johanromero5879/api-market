from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import routes
from app.user.infrastructure import user_routes
from app.auth.infrastructure import auth_routes

# App setup
app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Config routes
app.include_router(user_routes.router)
app.include_router(auth_routes.router)


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/pages/api.html")

