from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from parser import parse_user_input

app = FastAPI(title="NLP Service", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class ParseRequest(BaseModel):
    message: str


@app.post("/parse")
def parse(payload: ParseRequest):
    return parse_user_input(payload.message)
