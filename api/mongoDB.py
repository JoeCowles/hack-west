import os
from dotenv import load_dotenv
from pymongo import MongoClient
import dns.resolver

load_dotenv()

# Set custom DNS servers
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google's DNS servers
from pymongo.server_api import ServerApi

mongoPassword = os.getenv("PUBLIC_MONGODB_PWD")
connection_string = f"mongodb+srv://nathanschober25:{mongoPassword}@core.fs1nb.mongodb.net/?retryWrites=true&w=majority&appName=Core"
client = MongoClient(connection_string)
Db = client.Core
collection = Db.Users

def check_hashdb(pass_hash: str):
    collection = (
        Db.Users
    )  # Checks the user table and finds the user id of the user with the given pass_hash
    user_id = collection.find_one({"password": pass_hash})

    return str(user_id["_id"])



#seters
def signupdb(email: str, pass_hash: str):
    # return the status of the signup
    collection = Db.Users

    data1 = {"email": email, "password": pass_hash}
    print(data1)
    insert_result = collection.insert_one(data1)
    user_id = str(insert_result.inserted_id)
    print(user_id)
    return {"user_id": user_id, "status": "good"}
    # Return good if the signup is successful, return bad if the signup is unsuccessful


def logindb(email: str, pass_hash: str):
    collection = Db.Users
    # return the status of the login
    if collection.find_one({"email": email}):
        user = collection.find_one({"email": email})
        if user["password"] == pass_hash:
            # Return good if the login is successful
            return {"user_id": str(user["_id"]), "status": "good"}

    # return bad if the login is unsuccessful
    return {"status": "bad"}
def mkSyllabusdb(topic: str, description: str, user_id):
    collection = Db.sylabus
    data = {
        "foreign key": user_id,
        "topic": topic,
        "description": description
    }
    syb = collection.insert_one(data)
    return syb["_id"], {"status": "good"}
def mkLecturedb(description: str, video_id: str, syllabus_id):
    collection = Db.lecture
    data = {
        "foreign key": syllabus_id,
        "description": description,
        "video_id": video_id
    }
    lecture = collection.insert_one(data)
    return lecture["_id"], {"status": "good"}
def mkQuizdb(lecture_id: str):
    collection = Db.quiz
    data = {
        "foreign key": lecture_id
    }
    quiz = collection.insert_one(data)
    return quiz["_id"], {"status": "good"}
def mkQuestionb(quiz_id: str, questions: str, answers):
    collection = Db.questions
    data = {
        "foreign key": quiz_id,
        "questions": questions,
        "answers": answers
    }
    question = collection.insert_one(data)
    return question["_id"], {"status": "good"}


#geters
def check_hashdb(pass_hash: str):
    collection = Db.Users# Checks the user table and finds the user id of the user with the given pass_hash
    user_id = collection.find_one({"password": pass_hash})
    
    return user_id["_id"] 
def getsyllabus(mark):
    sylabus = Db.syllabus
    return sylabus.find_one({"_id": mark})
def getLecture(mark):
    lecture = Db.syllabus
    return lecture.find_one({"_id": mark})
def getQuiz(mark):
    quiz = Db.syllabus
    return quiz.find_one({"_id": mark})
def getQuestion(mark):
    question = Db.syllabus
    return question.find_one({"_id": mark})