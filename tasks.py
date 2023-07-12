import os
import db
import pytz
import threading
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta

load_dotenv()

client = MongoClient(os.environ.get('MONGO_URI'))
db_remote = client.get_database(os.environ.get('DB'))
user_collections = db_remote.get_collection("user")


def delete_old_users():
    cutoff_time = datetime.now() - timedelta(hours=24)
    print(cutoff_time)
    old_users = list(user_collections.find(
        {'created_at': {'$lt': cutoff_time}}))
    print(old_users)
    if old_users:
        for user in old_users:
            db.delete_user(user['_id'])


start_time = datetime.now()
print("Task Starting",)
delete_old_users()
end_time = datetime.now()
print("Task Ended\nTime Taken:", (end_time-start_time).seconds)
