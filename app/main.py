from fastapi import FastAPI
from .routers import models


app = FastAPI()


app.include_router(models.router)


@app.get("/")
def connection_check():
    return "Connection OK"
