from os import getenv
import uvicorn

# Assign 3000 port by default
PORT: int = int(getenv("PORT")) if bool(getenv("PORT")) else 3000

if __name__ == "__main__":
    uvicorn.run("app:app", port=PORT, reload=True)
