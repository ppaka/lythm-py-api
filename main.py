import requests
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = "https://discord.com/api/v10"
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8686"
app = FastAPI()


class ExchangeCodeRequestItem(BaseModel):
    code: str

class RefreshTokenRequestItem(BaseModel):
    refresh_token: str


def exchange_code(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8686",
    }
    response = requests.post("https://discord.com/api/v10/oauth2/token", data=data)
    return response.json()


def refresh_token(refresh_token: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post("https://discord.com/api/v10/oauth2/token", data=data)
    return response.json()


@app.post("/api/exchange/")
def exchange(item: ExchangeCodeRequestItem):
    return exchange_code(item.code)


@app.post("/api/refresh/")
def refresh(item: RefreshTokenRequestItem):
    return refresh_token(item.refresh_token)
