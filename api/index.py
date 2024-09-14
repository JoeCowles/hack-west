from fastapi import FastAPI
import dotenv
import uvicorn
import os
from pymongo import MongoClient
from . import gen_syllabus
from fastapi import Depends
import googleapiclient.discovery
import json
import youtube_transcript_api

DEFAULT_LANG = 'en-us'

YouTubeTranscriptApi = dotenv.load_dotenv(dotenv.find_dotenv("GoogleAPI_PWD"))
app = FastAPI()

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

dotenv.load_dotenv()

# Takes in a topic string and returns the ID of the top video
def get_video_id(topic: str) -> str:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("GoogleAPI_PWD")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="id",
        q=f"{topic}",
        maxResults=1,
        order="viewCount",
        type="video",
        videoCaption="closedCaption",
        videoEmbeddable="true"
    )
    response = request.execute()

    return response["items"][0]["id"]["videoId"]

def get_transcript(video_id: str):
    transcript_dict_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
    transcript_list = [d["text"] for d in transcript_dict_list]
    transcript = ''
    for line in transcript_list:
        transcript += line + ' '
    return transcript

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


@app.post("/create-course")
def create_course(prompt: str, user_id=Depends(check_hash)):
    syllabus = gen_syllabus.create_syllabus(prompt)
    print(syllabus)
    # Next, Create the lessons.
    return ""


@app.get("/get-courses")
def get_courses(user_id=Depends(check_hash)):

    # TODO: return the courses for the user
    return {"courses": []}

def get_videos(response):
    j = json.dumps(response)
    return response

@app.get("/")
def health_check():
    query = 'intro to proofs'
    video_id=get_video_id('intro to proofs')
    transcript = get_transcript(video_id)
    return {"status": "ok", "query": query, "video id": video_id, "transcript": transcript}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
