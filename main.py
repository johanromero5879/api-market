import uvicorn
from app.config import PORT


if __name__ == "__main__":
    uvicorn.run("app:app", port=PORT, reload=True)
