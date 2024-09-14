from fastapi import FastAPI
import dotenv
import uvicorn
import os
from pymongo import MongoClient
from .gen_syllabus import create_syllabus
from fastapi import Depends
import json
from fastapi.middleware.cors import CORSMiddleware
from . import gen_syllabus
from . import yt_api

DEFAULT_LANG = 'en-us'

google_key = dotenv.load_dotenv(dotenv.find_dotenv("GoogleAPI_PWD"))
app = FastAPI()

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

dotenv.load_dotenv()

# Set up CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mongoPassword = str(os.environ.get("PUBLIC_MONGODB_PWD"))

connection_string = (
    f"mongodb+srv://nathanschober25:{mongoPassword}@core.fs1nb.mongodb.net/"
)
client = MongoClient(connection_string)


Db = client.Core
collection = Db.Users
# collections = Db.list_collection_names()
data1 = {"email": "jon22@gmail.com", "password": "pass"}
collection.insert_one(data1)


def check_hash(pass_hash: str):
    collection = (
        Db.Users
    )  # Checks the user table and finds the user id of the user with the given pass_hash
    user_id = collection.find_one({"password": pass_hash})
    if user_id:
        return user_id["_id"]


check_hash("reee")


@app.post("/signup")
def signup(email: str, pass_hash: str):
    # return the status of the signup
    collection = Db.Users

    data1 = {"email": email, "password": pass_hash}

    user_id = collection.insert_one(data1)

    return user_id.inserted_id, {"status": "good"}
    # Return good if the signup is successful, return bad if the signup is unsuccessful


@app.post("/login")
def login(email: str, pass_hash: str):
    collection = Db.Users
    # return the status of the login
    if collection.find_one({"email": email}):
        user = collection.find_one({"email": email})
        if user["password"] == pass_hash:
            # Return good if the login is successful
            return user["_id"], {"status": "good"}

    # return bad if the login is unsuccessful
    return {"status": "bad"}


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
    query = 'taylor series'
    video_id=yt_api.get_video_id(query)
    transcript = yt_api.get_transcript(video_id)
    return {"status": "ok", "query": query, "video id": video_id, "transcript": transcript}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
