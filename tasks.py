import os
import db
import time
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
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    cutoff_time = cutoff_time.replace(tzinfo=pytz.UTC)
    old_users = list(user_collections.find(
        {'created_at': {'$lt': cutoff_time}}))
    if old_users:
        for user in old_users:
            db.delete_user(user['_id'])


def backgroud_task_1():
    while True:
        delete_old_users()
        time.sleep(86400)


threading.Thread(target=backgroud_task_1).start()
print("task running")
