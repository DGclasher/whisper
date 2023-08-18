#!/usr/bin/env python3

from db import users_collection, delete_user
from datetime import datetime, timedelta

def delete_old_users():
    current_time = datetime.now()
    threshold_time = current_time - timedelta(days=30)
    old_users = users_collection.find({'created_at': {'$lt': threshold_time}})
    deleted_count = 0
    for user in old_users:
        delete_user(user['_id'])
        deleted_count += 1

    print(f"Number of users deleted: {deleted_count}")

if __name__ == "__main__":
    delete_old_users()
