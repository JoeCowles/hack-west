from fastapi import FastAPI
import dotenv
import uvicorn
import os
from pymongo import MongoClient
from .gen_syllabus import create_syllabus
from .gen_quiz import create_quiz
from fastapi import Depends
import json
from fastapi.middleware.cors import CORSMiddleware
from . import yt_api

from .mongoDB import logindb, check_hashdb, signupdb, mkSyllabusdb, mkLecturedb, mkQuizdb, mkQuestiondb




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
        if len(lesson['link'].split("v=")) > 1:
            video_id = lesson['link'].split("v=")[1]
        else:
            video_id = lesson['link']

        video_id = video_id.replace("https://www.youtube.com/watch?v=", "")
        # Create the lecture 
        print(lesson)
        print(lesson['topic'], video_id, syllabus_id) 
        lesson['id'] = mkLecturedb(lesson['topic'], video_id, syllabus_id)
        lesson['video_id'] = video_id

    for lesson in lessons:
        quiz_id = mkQuizdb(lesson['id'])
        lesson['quiz_id'] = quiz_id

    for lesson in lessons:
        transcript = yt_api.get_transcript(lesson['video_id'], lesson['topic'])
        lesson['transcript'] = transcript
        print("Transcript: ", transcript[:100])
        quiz = create_quiz(transcript)
        while quiz['quiz'] == None:
            quiz = create_quiz(transcript)
        print("Quiz: ", quiz)
        for question in quiz['quiz']:
            if question['type'] == 'multiple-choice':
                question_text = question['question']
                answers = question['choices']
                correct_answer = question['correct-answer']
            elif question['type'] == 'true-false':
                question_text = question['question']
                answers = ['True', 'False']
                correct_answer = 0 if question['answer'] == 'True' else 1
        
            mkQuestiondb(lesson['quiz_id'], question_text, {
                'choices': answers,
                'correct_answer': correct_answer
            })

    print(syllabus_id)
    # Next, Create the lessons.
    return {"syllabus_id": str(syllabus_id)}




@app.get("/get-courses")
def get_courses(user_id=Depends(check_hash)):

    # TODO: return the courses for the user
    return {"courses": []}


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/test-yt")
async def test_yt():
    prompt = "Teach me how to solve a complex differential equation, starting from a college algebra level"
    syllabus = create_syllabus(prompt)
    lessons = await yt_api.create_lesson_plan(syllabus)
    print ('Lessons (JSON?): ', lessons)
    # TODO: This is only generating the first quiz, and since lessons is a list now it doesn't work
    transcripts = []
    quizzes = []
    for lesson in lessons:
        transcript = yt_api.get_transcript(yt_api.id_from_url(lesson["link"]))
        transcripts.append(transcript)
        quiz = create_quiz(transcript)
        quizzes.append(quiz)
    return {"prompt": prompt, "syllabus": syllabus, "lesson": lessons, "transcripts": transcripts, "quizzes": quizzes}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
