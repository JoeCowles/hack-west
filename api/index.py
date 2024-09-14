from fastapi import FastAPI
import uvicorn

app = FastAPI()

import os

import googleapiclient.discovery
import dotenv

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

dotenv.load_dotenv()

def test_youtube_api():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YouTube_PWD")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="id",
        q="Youtube Data API"
    )
    response = request.execute()

    return response

@app.get("/")
def health_check():
    youtube_response=test_youtube_api()
    return {"status": "ok", "response": youtube_response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
