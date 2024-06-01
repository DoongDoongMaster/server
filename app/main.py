import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth

from fastapi import FastAPI
from .routers import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Firebase Admin 초기화
cred = credentials.Certificate(os.environ["FIREBASE_CREDENTIAL"])
firebase_admin.initialize_app(cred)

app = FastAPI()

app.include_router(models.router)

@app.get("/")
def connection_check():
    return "Connection OK"