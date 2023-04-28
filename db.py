import os
from user import User
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash

load_dotenv()

client = MongoClient(os.environ.get('MONGO_URI'))

db = client.get_database(os.environ.get("DB"))
users_collection = db.get_collection("users")
rooms_collection = db.get_collection("rooms")
members_collection = db.get_collection("room_members")


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


def delete_user(username):
    users_collection.delete_one({'_id': username})
    members_collection.delete_many({'_id': {'username': username}})


def save_room(room_name, creator):
    room_data = {
        'room_name': room_name,
        'created_by': creator,
        'created_at': datetime.utcnow()
    }
    room_id = rooms_collection.insert_one(room_data).inserted_id
    add_room_member(room_id, room_name, creator, creator, is_room_admin=True)
    return room_id


def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    member = {
        '_id': {'room_id': ObjectId(room_id), 'username': username},
        'room_name': room_name,
        'added_by': added_by,
        'added_at': datetime.now(),
        'is_room_admin': is_room_admin
    }
    members_collection.insert_one(member)


def add_room_members(room_id, room_name, usernames, added_by):
    members = [{
        '_id': {'room_id': ObjectId(room_id), 'username': username},
        'room_name': room_name,
        'added_by': added_by,
        'added_at': datetime.now(),
        'is_room_admin': False
    } for username in usernames]

    members_collection.insert_many(members)


def remove_room_members(room_id, usernames):
    members_collection.delete_many(
        {'_id': {'$in': [{'room_id': room_id, 'username': username} for username in usernames]}})


def update_room(room_id, room_name):
    rooms_collection.update_one({'_id': ObjectId(room_id)}, {
                                '$set': {'room_name': room_name}})


def get_room(room_name):
    return dict(rooms_collection.find_one({'room_name': room_name}))


def delete_room(room_name):
    rooms_collection.delete_one({'room_name': room_name})
    members_collection.delete_many({'room_name': room_name})


def get_room_members(room_id):
    return list(members_collection.find({'_id.room_id': ObjectId(room_id)}))


def get_rooms_for_user(username):
    return list(rooms_collection.find({'created_by': username}))


def is_room_member(room_id, username):
    return members_collection.count_documents(
        {'_id': {'room_id': ObjectId(room_id), 'username': username}})


def is_room_admin(room_id, username):
    members_collection.count_documents({'_id': {'room_id': ObjectId(
        room_id), 'username': username}, 'is_room_admin': True})
