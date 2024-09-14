import os
from dotenv import load_dotenv
from pymongo import MongoClient
import dns.resolver

load_dotenv()

# Set custom DNS servers
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google's DNS servers

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
