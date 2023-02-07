from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import routes
# IMPORTANT: Put new routes always at top because circular import error with middlewares
from app.purchase.infrastructure import purchase_routes
from app.product.infrastructure import product_routes
from app.user.infrastructure import user_routes
from app.auth.infrastructure import auth_routes

from containers import Container

# Dependency Injection Container
container = Container()
container.config.services.jwt.secret.from_env("JWT_SECRET")
container.config.gateways.database.uri.from_env("MONGO_URI")
container.check_dependencies()

# App setup
app = FastAPI()
app.container = container

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Config routes
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(purchase_routes.router)


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/pages/api.html")
