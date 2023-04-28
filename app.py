import os
import db
import secrets
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, join_room, leave_room
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='./static', static_url_path='/static')
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)
load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    rooms = []
    if current_user.is_authenticated:
        rooms = db.get_rooms_for_user(current_user.username)
    return render_template('home.html', current_user=current_user, rooms=rooms)


@app.route('/join')
@login_required
def join():
    return render_template('join.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.get_user(username)

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = 'Incorrect credentials'
            return render_template('login.html', message=message)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            db.save_user(username, password)
        except DuplicateKeyError:
            message = 'User with that username exists'
            return render_template('register.html', message=message)

        login_user(db.get_user(username))
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    message = ''
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        usernames = [username.strip()
                     for username in request.form.get('members').split(',')]
        if len(room_name) and len(usernames):
            room_id = db.save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            db.add_room_members(room_id, room_name,
                                usernames, current_user.username)
            return redirect(url_for('home'))
        else:
            message = 'Failed to create room'
            return render_template('create_room.html', message=message)
    return render_template('create_room.html')


@app.route('/del_room/<room_name>', methods=['POST'])
@login_required
def del_room(room_name):
    if request.method == 'POST':
        if room_name:
            room = db.get_room(room_name)
            if room['created_by'] == current_user.username:

                db.delete_room(room_name)
                print("room deleted")
                return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.route('/chat/<room_name>/', methods=['POST'])
def chat(room_name):
    username = request.form["username"]
    try:
        room = db.get_room(room_name)
        if room and db.is_room_member(str(room['_id']), current_user.username):
            return render_template('chat.html', username=username, room=room, current_user=current_user)
    except:
        message = "Unable to join that room"
        return (url_for('home', message=message))
    return redirect(url_for('home'))


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit('join_room', data, room=room)
    app.logger.info("{} has joined {}".format(username, room))


@socketio.on('send_message')
def on_send_message(data):
    app.logger.info("{} in room {} has sent message {}".format(
        data['username'], data['room'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('leave')
def on_leave(data):
    print('on_leave called')  # Debugging line
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.emit(
        'leave_room', {'username': username, 'room': room}, room=room)
    return redirect(url_for('home', current_user=current_user))


@login_manager.user_loader
def load_user(username):
    return db.get_user(username)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, port=port, debug=True)
