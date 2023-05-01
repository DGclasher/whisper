import os
from user import User
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient, ASCENDING, DESCENDING
from werkzeug.security import generate_password_hash

load_dotenv()

client = MongoClient(os.environ.get('MONGO_URI'))

db = client.get_database(os.environ.get("DB"))
users_collection = db.get_collection("users")
rooms_collection = db.get_collection("rooms")
try:
    rooms_collection.drop_index('room_name_1')
except:
    pass
rooms_collection.create_index([('room_name', ASCENDING)], unique=True)
members_collection = db.get_collection("room_members")
messages_collection = db.get_collection("messages")


def save_user(username, password):
    hashed_pass = generate_password_hash(password)
    user_data = {
        '_id': username,
        'password': hashed_pass,
        'created_at': datetime.now()
    }
    users_collection.insert_one(user_data)


def get_user(username):
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['password'], user_data['created_at']) if user_data else None


def delete_user(username):
    users_collection.delete_one({'_id': username})
    rooms_collection.delete_many({'created_by': username})
    members_collection.delete_many({'_id.username': username})
    messages_collection.delete_many({'sender': username})


def save_room(room_name, creator):
    room_data = {
        'room_name': room_name,
        'created_by': creator,
        'created_at': datetime.now()
    }
    try:
        room_id = rooms_collection.insert_one(room_data).inserted_id
        add_room_member(room_id, room_name, creator,
                        creator, is_room_admin=True)
        return room_id
    except DuplicateKeyError:
        return None


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
    room = rooms_collection.find_one({'room_name': room_name})
    messages_collection.delete_many({'room_id': str(room['_id'])})
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
    return members_collection.count_documents({'_id': {'room_id': ObjectId(
        room_id), 'username': username}, 'is_room_admin': True})


def save_message(room_id, text, sender):
    message = {
        'room_id': room_id,
        'text': text,
        'sender': sender,
        'sent_at': datetime.now()
    }
    messages_collection.insert_one(message)


MESSAGE_LIMIT = 10

def get_messages(room_id, page=0):
    offset = page * MESSAGE_LIMIT
    mes = list(messages_collection.find({'room_id': room_id}).sort(
        'sent_at', ASCENDING).limit(MESSAGE_LIMIT).skip(offset))
    for m in mes:
        m['sent_at'] = m['sent_at'].strftime("%d/%b:%H:%M")
    return mes
