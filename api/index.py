from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
import uvicorn
import os
from pymongo import MongoClient
YouTubeTranscriptApi = load_dotenv(find_dotenv("YouTubeAPI_PWD"))
app = FastAPI()

load_dotenv()
mongoPassword = str(os.environ.get("PUBLIC_MONGODB_PWD"))

connection_string = "mongodb+srv://nathanschober25:{mongoPassword}@core.fs1nb.mongodb.net/"
client = MongoClient(connection_string)


Db = client.Core
collection = Db.Users
# collections = Db.list_collection_names()
data1 = {
    "email": "jon22@gmail.com",
    "password": "pass"
    }
collection.insert_one(data1)



def check_hash(pass_hash: str):
    collection = Db.Users# Checks the user table and finds the user id of the user with the given pass_hash
    user_id = collection.find_one({"password": pass_hash})
    if user_id:
        return user_id["_id"]
    

@app.post("/signup")
def signup(email: str, pass_hash: str):
    # return the status of the signup
    collection = Db.Users

    data1 = {
    "email": email, 
    "password": pass_hash
    }

    user_id = collection.insert_one(data1)

    return user_id.inserted_id, {"status": "good"}
    # Return good if the signup is successful, return bad if the signup is unsuccessful


@app.post("/login")
def login(email: str, pass_hash: str):
    collection = Db.Users
    # return the status of the login
    if collection.find_one({"email": email}):
        user = collection.find_one({"email": email})
        if user["password"] == pass_hash:
            # Return good if the login is successful
            return user["_id"], {"status": "good"}
        
    # return bad if the login is unsuccessful
    return {"status": "bad"}

@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
