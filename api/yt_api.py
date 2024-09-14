import googleapiclient.discovery
import youtube_transcript_api
from .video_search import search_videos
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("GoogleAPI_PWD")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def get_transcript(video_id: str):
    transcript_dict_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
    transcript_list = [d["text"] for d in transcript_dict_list]
    transcript = ''
    for line in transcript_list:
        transcript += line + ' '
    return transcript

async def create_lesson_plan(syllabus):
    video_ids = []
    for lesson in syllabus["lessons"]:
        print(type(lesson["topic"]))
        print(lesson["topic"])
        id = await search_videos(lesson["topic"])
        print(id)
        video_ids.append(id)
    return video_ids