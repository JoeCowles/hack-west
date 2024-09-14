from fastapi import FastAPI
import dotenv
import uvicorn
import os
from pymongo import MongoClient
from .gen_syllabus import create_syllabus
from fastapi import Depends
import json
from fastapi.middleware.cors import CORSMiddleware
from . import yt_api
from .mongoDB import logindb, check_hashdb, signupdb

DEFAULT_LANG = "en-us"

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


def check_hash(pass_hash: str):
    return check_hashdb(pass_hash)


@app.post("/signup")
def signup(email: str, pass_hash: str):
    return signupdb(email, pass_hash)


@app.post("/login")
def login(email: str, pass_hash: str):
    return logindb(email, pass_hash)


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
    return {"status": "ok"}

@app.get("/test")
async def test_yt():
    prompt = "i want to learn about the taylor series"
    syllabus = create_syllabus(prompt)
    lessons = await yt_api.create_lesson_plan(syllabus)
    return {"lessons": lessons, "syllabus": syllabus}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
