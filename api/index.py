from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import uvicorn
import os
from pymongo import MongoClient

YouTubeTranscriptApi = load_dotenv(find_dotenv("YouTubeAPI_PWD"))
app = FastAPI()

MongoPassword = os.environ.get("MONGODB_PWD")
connection_string = "mongodb+srv://nathanschober25:{MongoPassword}@core.fs1nb.mongodb.net/?retryWrites=true&w=majority&appName=Core"
client = MongoClient(connection_string)


def check_hash(pass_hash: str):
    # Checks the user table and finds the user id of the user with the given pass_hash
    return "user id"


@app.post("/signup")
def signup(email: str, pass_hash: str):
    # return the status of the signup
    return {"status": "ok"}
    # Return good if the signup is successful, return bad if the signup is unsuccessful


@app.post("/login")
def login(email: str, pass_hash: str):
    # return the status of the login
    return {"status": "ok"}
    # Return good if the login is successful, return bad if the login is unsuccessful


@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
