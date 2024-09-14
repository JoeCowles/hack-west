from fastapi import FastAPI
import dotenv
import uvicorn
import os
from pymongo import MongoClient
import googleapiclient.discovery

YouTubeTranscriptApi = dotenv.load_dotenv(dotenv.find_dotenv("YouTubeAPI_PWD"))
app = FastAPI()


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

dotenv.load_dotenv()

def test_youtube_api():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YouTubeAPI_PWD")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="id,snippet",
        q="Youtube Data API"
    )
    response = request.execute()

    return response

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

def get_videos(response):
    print(type(response))
    return response['items']

@app.get("/")
def health_check():
    youtube_response=test_youtube_api()
    videos=get_videos(youtube_response)
    return {"status": "ok", "\nvideos": videos}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
