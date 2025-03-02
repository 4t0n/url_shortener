import uvicorn
from fastapi import FastAPI

from app.api.endpoints.shortener import links_router


app = FastAPI()

app.include_router(links_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app")
