from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()

genai.configure(api_key=os.environ["GoogleAPI_PWD"])

# Create the model
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192*2,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction='You are a bot created to create quizzes based on a transcript of a video about a topic. You will be provided with the entirety of the transcript. Your job is to identify the most important key points of the transcript in order to make both true/false and multiple choice quiz questions. Your output should look like this JSON format:\n{"quiz": [{"type": "multiple-choice","question": "This is where the question goes","choices": ["This is where option A goes","This is where option B goes","This is where option C goes","This is where option D goes"],"correct-answer": "This is where the index (from 0-3) of the correct answer choice goes"}, {"type": "true-false","question": "This is where the question goes","answer": "Put either True or False here depending on the answer"}]}\n\nThere should be between 1-3 multiple choice question objects and between 1-3 true/false question objects. The number of questions should add up to 15. The questions should be be able to be answered based only on the information provided in the transcript. If there isn\'t a transcript, then just make a short general quiz based on the topic provided. Keep the total number of questions under 5!\n',
)

chat_session = model.start_chat(history=[])

# I have fucking given up. I am going to just run this 3 times until it works. If it doesn't work then all hope is lost, God is dead
# the Easter Bunny is fake, Santa is giving everyone coal, and Brazzers is no longer giving free trials.
def create_quiz(transcript: str, tries=3):
    try:
        msg = chat_session.send_message(transcript).text
        print (f'\n\nQUIZ RESULT (attempt {4 - tries}): ', msg.replace('\n', ' '))
        # Parse the message to JSON. Remove the outer ```JSON tags
        # Encode and decode to remove any non-utf-8 characters
        json_msg = msg.encode('utf-8', 'ignore').decode('utf-8')
        json_msg = msg.strip("```json").strip("```JSON").strip("```")
        return json.loads(json_msg)
    except:
        if (tries == 0):
            return None
        else:
            return create_quiz(transcript, tries-1)
