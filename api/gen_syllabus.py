from dotenv import load_dotenv
import os
import google.generativeai as genai
import json

load_dotenv()

genai.configure(api_key=os.environ["NEXT_PUBLIC_GEMINI_API_KEY"])


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
    system_instruction='You are a bot created to plan academic courses on a topic. The user will give you the topic that they want to learn. your job is to write  a syllabus for the course. Your output should look like this JSON format:\n{\n"topic" : "topic the user is studying",\n"desc" : "A fully written out description of what the user will learn."\n"lessons": [\n{\n"topic" : "lesson topic",\n}\n]\n}\n\nThe lesson topics should be VERY precise. Write out the exact topic that the user should learn for that topic. Each course should have 15-20 lessons depending on topic complexity. \n',
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "I want to learn about programming in c \n",
            ],
        },
        {
            "role": "model",
            "parts": [
                '{\n"topic" : "Programming in C",\n"desc" : "This course provides a comprehensive introduction to programming using the C language. Starting with the fundamentals, you will learn how to write, compile, and debug C programs. You will explore key concepts such as data types, operators, control flow, functions, arrays, pointers, and memory management. The course also covers more advanced topics like file handling, data structures, and algorithms. By the end, you will be able to write efficient, well-structured C code for a variety of applications.",\n"lessons": [\n{\n"topic" : "Introduction to Programming and C"\n},\n{\n"topic" : "Setting up Your C Development Environment"\n},\n{\n"topic" : "Basic Syntax, Data Types, and Variables"\n},\n{\n"topic" :  "Operators and Expressions in C"\n},\n{\n"topic" :  "Input and Output Operations (printf and scanf)"\n},\n{\n"topic" : "Control Flow Statements: if, else, switch"\n},\n{\n"topic" : "Looping Structures: for, while, do-while"\n},\n{\n"topic" : "Functions: Declaration, Definition, and Usage"\n},\n{\n"topic" : "Arrays: Understanding and Working with Arrays"\n},\n{\n"topic" :  "Pointers in C: Concepts and Applications"\n},\n{\n"topic" :  "Strings: Character Arrays and String Manipulation"\n},\n{\n"topic" : "Memory Management: Dynamic Allocation (malloc, calloc, free)"\n},\n{\n"topic" : "Structures: Creating and Using Structures"\n},\n{\n"topic" :  "File Handling in C: Reading and Writing Files"\n},\n{\n"topic" :  "Preprocessing Directives: #include, #define, Macros"\n},\n{\n"topic" :  "Basic Debugging Techniques in C"\n}\n]\n}',
            ],
        },
    ]
)


def create_syllabus(prompt: str):
    msg = chat_session.send_message(prompt).text
    # Parse the message to JSON. Remove the outer ```JSON tags
    json_msg = msg.strip("```JSON").strip("```")
    return json.loads(json_msg)
