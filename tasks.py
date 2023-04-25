import os
import time
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.environ.get('MONGO_URI'))
db = client.get_database(os.environ.get('DB'))
user_collections = db.get_collection("user")


def delete_old_users():
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    user_collections.delete_many({'created_at': {'$lt': cutoff_time}})


def backgroud_task_1():
    while True:
        delete_old_users()
        time.sleep(86400)


threading.Thread(target=backgroud_task_1).start()
