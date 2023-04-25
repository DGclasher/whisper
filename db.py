import os
from user import User
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash

load_dotenv()

client = MongoClient(os.environ.get('MONGO_URI'))

db = client.get_database(os.environ.get("DB"))
users_collection = db.get_collection("users")


def save_user(username, password):
    hashed_pass = generate_password_hash(password)
    user_data = {
        '_id': username,
        'password': hashed_pass,
        'created_at': datetime.utcnow()
    }
    users_collection.insert_one(user_data)


def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['password']) if user_data else None

