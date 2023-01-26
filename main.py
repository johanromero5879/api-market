from os import getenv

from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    PORT: int = int(getenv("PORT")) if bool(getenv("PORT")) else 3000
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
