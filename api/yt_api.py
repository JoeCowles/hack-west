import googleapiclient.discovery
import youtube_transcript_api
from .video_search import search_videos
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import json

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
load_dotenv()
DEVELOPER_KEY = os.getenv("GoogleAPI_PWD")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def id_from_url(url: str) -> str:
    # Parse the URL
    parsed_url = urlparse(url)
    
    # If the video ID is in the query parameters (common case)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        video_id = parse_qs(parsed_url.query).get('v')
        if video_id:
            return video_id[0]
    
    # If the video ID is in the path (shortened URL case)
    elif parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]
    
    # If the URL does not match a YouTube video format
    return None

def get_transcript(video_id: str, topic: str):
    transcript_dict_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
        video_id
    )
    transcript_list = [d["text"] for d in transcript_dict_list]
    transcript = ""
    for line in transcript_list:
        transcript += line + " "
    # If the transcript is empty, return the topic, the ai will generate a quiz based on the topic
    if transcript == "":
        return topic
    return transcript


async def create_lesson_plan(syllabus):
    video_ids = []
    for lesson in syllabus["lessons"]:
        print(type(lesson["topic"]))
        print(lesson["topic"])
        id = await search_videos(lesson["topic"])
        if id:
            id['topic'] = lesson['topic']
        else:
            continue
        # Replace the problematic print statement with this:
        print()
        # Ensure proper JSON serialization
        id = json.dumps(id, ensure_ascii=False)
        # Parse the id back to JSON
        id = json.loads(id)
        video_ids.append(id)
    return video_ids
