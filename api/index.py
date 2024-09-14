from fastapi import FastAPI
import dotenv
import uvicorn
import os
from pymongo import MongoClient
from .gen_syllabus import create_syllabus
from fastapi import Depends
import googleapiclient.discovery
import json
from .mongoDB import check_hashdb, signupdb, logindb

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


mongoPassword = str(os.environ.get("PUBLIC_MONGODB_PWD"))
connection_string = f"mongodb+srv://nathanschober25:{mongoPassword}@core.fs1nb.mongodb.net/"
client = MongoClient(connection_string)


Db = client.Core
collection = Db.Users


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

def get_videos(response):
    j = json.dumps(response)
    return response

@app.get("/")
def health_check():
    video_id=get_video_id('intro to proofs')
    return {"status": "ok", "video id": video_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
