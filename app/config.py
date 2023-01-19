from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Session
JWT_SECRET = getenv("JWT_SECRET")
if not JWT_SECRET:
    raise AttributeError("JWT_SECRET not found")

# Server
PORT: int = int(getenv("PORT")) if bool(getenv("PORT")) else 3000


# Databases
MONGO_URI = getenv("MONGO_URI")
