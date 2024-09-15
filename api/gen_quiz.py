from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()

genai.configure(api_key=os.environ["GoogleAPI_PWD"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192*2,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction='You are a bot created to create quizzes based on a transcript of a video about a topic. You will be provided with the entirety of the transcript. Your job is to identify the most important key points of the transcript in order to make both true/false and multiple choice quiz questions. Your output should look like this JSON format:\n{"quiz": [{"type": "multiple-choice","question": "This is where the question goes","choices": ["This is where option A goes","This is where option B goes","This is where option C goes","This is where option D goes"],"correct-answer": "This is where the index (from 0-3) of the correct answer choice goes"}, {"type": "true-false","question": "This is where the question goes","answer": "Put either True or False here depending on the answer"}]}\n\nThere should be between 10-15 multiple choice question objects and between 5-10 true/false question objects. The questions should be be able to be answered based only on the information provided in the transcript.\n',
)

chat_session = model.start_chat(history=[])


def create_quiz(transcript: str):
    msg = chat_session.send_message(transcript).text
    print ('\n\nQUIZ RESULT: ', msg.replace('\n', ' '))
    # Parse the message to JSON. Remove the outer ```JSON tags
    # Encode and decode to remove any non-utf-8 characters
    json_msg = msg.encode('utf-8', 'ignore').decode('utf-8')
    json_msg = msg.strip("```json").strip("```JSON").strip("```")

    return json.loads(json_msg)
