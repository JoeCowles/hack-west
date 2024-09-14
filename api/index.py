from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import uvicorn
YouTubeTranscriptApi = load_dotenv(find_dotenv("YouTubeAPI_PWD"))YouTubeAPI_PWD
app = FastAPI()

@app.get("/GetTranscript")
def GetTranscript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ar"])

@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
