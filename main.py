from os import getenv
import asyncio

from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()


async def start_server(host:str, port: int):
    uvicorn.run("app:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    host: str = getenv("HOST") if getenv("HOST") else "127.0.0.1"
    port: int = int(getenv("PORT")) if getenv("PORT") else 3000

    asyncio.run(start_server(host, port))
