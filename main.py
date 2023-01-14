from app.config import PORT
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", port=PORT, reload=True)
