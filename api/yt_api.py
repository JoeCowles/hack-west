import googleapiclient.discovery
import youtube_transcript_api
import os

# Takes in a topic string and returns the ID of the top video
def get_video_id(topic: str) -> str:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("GoogleAPI_PWD")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.search().list(
        part="id",
        q=f"{topic}",
        maxResults=1,
        order="viewCount",
        type="video",
        videoCaption="closedCaption",
        videoEmbeddable="true",
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