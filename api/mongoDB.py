import os
from dotenv import load_dotenv
from pymongo import MongoClient
import dns.resolver
from bson import ObjectId
from pymongo.server_api import ServerApi
load_dotenv()

# Set custom DNS servers
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google's DNS servers

#establishing MongoDb connection
mongoPassword = os.getenv("PUBLIC_MONGODB_PWD")
MongoAPI = os.getenv("MongoAPI")
ApiKey = MongoAPI
connection_string = f"mongodb+srv://nathanschober25:{mongoPassword}@core.fs1nb.mongodb.net/?retryWrites=true&w=majority&appName=Core"
client = MongoClient(connection_string)

#assigning universal variables
Db = client.Core
collection = Db.Users

#seters
def signupdb(email: str, pass_hash: str):
    # return the status of the signup
    collection = Db.users

    data1 = {"email": email, 
            "password": pass_hash, 
            "syllabus": []
            }
    print(data1)
    insert_result = collection.insert_one(data1)
    user_id = str(insert_result.inserted_id)
    print(user_id)
    return {"user_id": user_id, "status": "good"}
    # Return good if the signup is successful, return bad if the signup is unsuccessful
def logindb(email: str, pass_hash: str):
    collection = Db.users
    # return the status of the login
    if collection.find_one({"email": email}):
        user = collection.find_one({"email": email})
        if user["password"] == pass_hash:
            # Return good if the login is successful
            return {"user_id": user["_id"], "status": "good"}

    # return bad if the login is unsuccessful
    return {"status": "bad"}
def mkSyllabusdb(topic: str, description: str, user_id):
    collection = Db.syllabus
    data = {
        "foreign_key": user_id,
        "topic": topic,
        "description": description,
        "lessons": []
    }
    syb = collection.insert_one(data)
    sybId = syb.inserted_id
    Db.user.update_one(
        {"_id": user_id,},
        {"$push": {"syllabus": sybId}}
    )
    return sybId
def mkLecturedb(description: str, video_id: str, syllabus_id):
    collection = Db.lecture
    data = {
        "foreign_key": syllabus_id,
        "description": description,
        "video_id": video_id,
        "quiz": []
    }
    lecture = collection.insert_one(data)
    lectureId = lecture.inserted_id
    Db.syllabus.update_one(
        {"_id": syllabus_id,},
        {"$push": {"lessons": lectureId}}
    )
    return lectureId
def mkQuizdb(lecture_id: str):
    collection = Db.quiz
    data = {
        "foreign_key": lecture_id,
        "questions": [],
        "score": 0.0
    }
    quiz = collection.insert_one(data)
    quizId = quiz.inserted_id
    Db.lecture.update_one(
        {"_id": lecture_id,},
        {"$push": {"quiz": quizId}}
    )
    return quizId
def mkQuestiondb(quiz_id: str, questions: str, answers):
    collection = Db.questions
    data = {
        "foreign_key": quiz_id,
        "questions": questions,
        "answers": answers
    }
    question = collection.insert_one(data)
    questionId = question.inserted_id
    Db.quiz.update_one( 
        {"_id": quiz_id,},
        {"$push": {"questions": questionId}}
    )
    return questionId

#get entire file (returns a dictionary)
# returns user _id
def check_hashdb(pass_hash: str):
    collection = (
        Db.users
    )  # Checks the user table and finds the user id of the user with the given pass_hash
    user_id = collection.find_one({"password": pass_hash})

    return str(user_id["_id"])
#  returns complete syllabus file
def getsyllabus(mark):
    sylabus = Db.syllabus
    return sylabus.find_one({"_id": mark})
# returns complete lecture file (from lessonId)
def getLecture(mark):
    lecture = Db.syllabus
    return lecture.find_one({"_id": mark})
# returns complete quiz file
def getQuiz(mark):
    quiz = Db.syllabus
    return quiz.find_one({"_id": mark})
# returns complete question file
def getQuestion(mark):
    question = Db.syllabus
    return question.find_one({"_id": mark})
#returns the score stored in quiz file (float)
def getScore(mark):
    quiz = Db.quiz
    quizCluster = quiz.find_one({"_id": mark})
    return quizCluster["score"]
#assignes passed value to score feild in quiz file
def updateScore(mark, grade):
    quiz = Db.quiz
    quiz.update_one(
        {"_id": mark},
        {"score": grade}
    )
    return 0

#get part of file
# returns id field of file passed (bson object)
def getId(clusterFile):
    return clusterFile["_id"]
# returns contents of description field (string)
def getDescription(clusterFile):
    return clusterFile["description"]
# returns contents of ForignKey feild (string)
def getForignKey(clusterFile):
    return clusterFile["forign_key"]
# returns contents of videoId feild (string)
def getVideoID(clusterFile):
    return clusterFile["video_id"]
# returns contents of Answers feild (string)
def getAnswers(clusterFile):
    return clusterFile["answers"]
# returns contents of question field (string)
def getQuestionTXT(clusterFile):
    return clusterFile["Questions"]
# returns contents of title feild (string)
def getsylabi(user_id):
    collection = Db.Users
    data = collection.find_one({"_id": user_id})
    return data["syllabus"]

def get_user_syllabi(user_id):
    collection = Db.syllabus
    syllabi = list(collection.find({"foreign_key": user_id}))
    return syllabi

def get_syllabus_lessons(syllabus_id):
    syllabus = Db.syllabus.find_one({"_id": ObjectId(syllabus_id)})
    if syllabus:
        lesson_ids = syllabus.get("lessons", [])
        lessons = list(Db.lecture.find({"_id": {"$in": lesson_ids}}))
        return lessons
    return []

def get_lesson_quiz_questions(lesson_id):
    lesson = Db.lecture.find_one({"_id": ObjectId(lesson_id)})
    print("LESSON", lesson)
    if lesson:
        quiz_ids = lesson.get("quiz", [])
        quizzes = list(Db.quiz.find({"_id": {"$in": quiz_ids}}))
        question_ids = [question_id for quiz in quizzes for question_id in quiz.get("questions", [])]
        questions = list(Db.questions.find({"_id": {"$in": question_ids}}))
        return questions
    return []