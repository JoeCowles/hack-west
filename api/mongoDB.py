import dotenv
import os
from pymongo import MongoClient


mongoPassword = str(os.environ.get("PUBLIC_MONGODB_PWD"))
connection_string = f"mongodb+srv://nathanschober25:{mongoPassword}@core.fs1nb.mongodb.net/"
client = MongoClient(connection_string)
Db = client.Core
collection = Db.Users


def check_hashdb(pass_hash: str):
    collection = Db.Users# Checks the user table and finds the user id of the user with the given pass_hash
    user_id = collection.find_one({"password": pass_hash})
    
    return user_id["_id"]
    
def signupdb(email: str, pass_hash: str):
    # return the status of the signup
    collection = Db.Users

    data1 = {
    "email": email, 
    "password": pass_hash
    }

    user_id = collection.insert_one(data1)

    return user_id.inserted_id, {"status": "good"}
    # Return good if the signup is successful, return bad if the signup is unsuccessful

def logindb(email: str, pass_hash: str):
    collection = Db.Users
    # return the status of the login
    if collection.find_one({"email": email}):
        user = collection.find_one({"email": email})
        if user["password"] == pass_hash:
            # Return good if the login is successful
            return user["_id"], {"status": "good"}
        
    # return bad if the login is unsuccessful
    return {"status": "bad"}
