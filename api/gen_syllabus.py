from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()

genai.configure(api_key=os.environ["GoogleAPI_PWD"])

safe = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safe,
    system_instruction='You are a bot created to plan academic courses on a topic. The user will give you the topic that they want to learn. your job is to write  a syllabus for the course. Your output should look like this JSON format:\n{\n"topic" : "topic the user is studying",\n"desc" : "A fully written out description of what the user will learn."\n"lessons": [\n{\n"topic" : "lesson topic",\n}\n]\n}\n\nThe lesson topics should be VERY precise. Write out the exact topic that the user should learn for that topic. Each course should have 15-20 lessons depending on topic complexity. YOU MUST ONLY RETURN JSON. Your json is directly loaded by json.loads(json_msg) so make sure the JSON is valid. Make sure to escape all characters that need to be escaped.\n',
)

chat_session = model.start_chat(history=[])


def create_syllabus(prompt: str):
    # Parse the message to JSON. Remove the outer ```JSON tags
    while True:
        msg = chat_session.send_message(prompt).text
        print('SYLLABUS JSON:', msg)
        json_msg = msg.strip("```JSON").strip("```").strip("```json")
        try:
            json_obj = json.loads(json_msg)
            return json_obj
        except Exception as e:
            print("ERROR PARSING JSON" + str(e))
            prompt = prompt + "Please try again, incorrect JSON format. ONLY RETURN JSON." + str(e)



        
