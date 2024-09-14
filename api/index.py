from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import uvicorn
import os
from pymongo import MongoClient
from .gen_syllabus import create_syllabus
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

YouTubeTranscriptApi = load_dotenv(find_dotenv("YouTubeAPI_PWD"))
app = FastAPI()

import os

import googleapiclient.discovery
import dotenv

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

dotenv.load_dotenv()


# Set up CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def test_youtube_api():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YouTube_PWD")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.search().list(part="id", q="Youtube Data API")
    response = request.execute()

    return response


# MongoPassword = os.environ.get("MONGODB_PWD")
# connection_string = "mongodb+srv://nathanschober25:{MongoPassword}@core.fs1nb.mongodb.net/?retryWrites=true&w=majority&appName=Core"
# client = MongoClient(connection_string)


def check_hash(pass_hash: str):
    # Checks the user table and finds the user id of the user with the given pass_hash
    return "user id"


@app.post("/signup")
def signup(email: str, pass_hash: str):
    # return the status of the signup
    return {"user_id": "id", "status": "good"}
    # Also return the user id
    # Return good if the signup is successful, return bad if the signup is unsuccessful


@app.post("/login")
def login(email: str, pass_hash: str):
    # return the status of the login
    return {"user_id": "id", "status": "good"}
    # Also return the user id
    # Return good if the login is successful, return bad if the login is unsuccessful


@app.post("/create-course")
def create_course(prompt: str, user_id=Depends(check_hash)):
    syllabus = create_syllabus(prompt)
    print(syllabus)
    # Next, Create the lessons.
    return ""


@app.get("/get-courses")
def get_courses(user_id=Depends(check_hash)):

    # TODO: return the courses for the user
    return {"courses": []}


@app.get("/")
def health_check():
    youtube_response = test_youtube_api()
    return {"status": "ok", "response": youtube_response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
