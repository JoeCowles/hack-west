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

from .mongoDB import logindb, check_hashdb, signupdb, mkSyllabusdb, mkLecturedb


DEFAULT_LANG = "en-us"

# oogle_key = dotenv.load_dotenv(dotenv.find_dotenv("GoogleAPI_PWD"))
google_key = os.getenv("GoogleAPI_PWD")
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
async def create_course(prompt: str, user_id: str):
    print(prompt)
    syllabus = create_syllabus(prompt)
    print(syllabus)
    syllabus_id = mkSyllabusdb(syllabus['topic'], syllabus['desc'], user_id)
    print(syllabus_id)
    lessons = await yt_api.create_lesson_plan(syllabus)
    print(lessons)
    for lesson in lessons:
        # Get the video id from the link
        video_id = lesson['link'].split("v=")[1]
        # Create the lecture 
        print(lesson)
        print(lesson['topic'], video_id, syllabus_id) 
        mkLecturedb(lesson['topic'], video_id, syllabus_id)

    #for lesson in lessons:
        #transcript = await yt_api.get_transcript(lesson.link)
        #lesson.transcript = transcript
        # Description, Syllabus_id, video_id    

    #print(syllabus)
    # Next, Create the lessons.
    return {"syllabus_id": syllabus_id}




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
