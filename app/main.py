import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()


app.include_router(models.router)


@app.get("/")
def connection_check():
    return "Connection OK"
