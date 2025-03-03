import uvicorn
from fastapi import FastAPI

from app.api.endpoints.shortener import links_router


app = FastAPI()

app.include_router(links_router)


@app.get("/")
async def start_page():
    return {"Message": "Test task for 5D"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8080)
