from flask import Flask, render_template, redirect, abort, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from collections import deque
from urlgen import urlgen
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ~'
socketio = SocketIO(app)

rooms = {}

######################
##  Route Handlers  ##
######################

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/create')
@app.route('/create/')
def show_create():
	# Generate a unique url suffix
	suffix = urlgen.generate()
	while suffix in rooms:
		suffix = urlgen.generate()
	# Create an empty room entry for this suffix
	rooms[suffix] = {
		'id': uuid.uuid4(),
		'suffix': suffix,
		'users': {}
	}
	return redirect('/' + suffix)

@app.route('/join')
@app.route('/join/')
def show_join():
	return render_template('join.html')

@app.route('/<roomname>')
def enter_room(roomname):
	# Serve room if it exists
	if roomname in rooms:
		return render_template("chatroom.html", roomname=roomname)
	else:
		return abort(404)

######################
##  Event Handlers  ##
######################

@socketio.on('connect')
def handle_connect():
	emit('response', {'data': 'user connected'})

@socketio.on('disconnect')
def handle_disconnect():
	emit('response', {'data': 'user connected'})

@socketio.on('join')
def handle_join(data):
	# Extract username, room, and session id
	username = data['username']
	room = data['room']
	if room not in rooms:
		return
	sid = request.sid
	# Map username to session id in room space
	rooms[room]['users'][sid] = username
	join_room(room)
	send(username + ' has entered the room.', room=room)

@socketio.on('message')
def handle_msg(data):
	room = data['room']
	sid = request.sid
	# Echo received messages back to room
	emit('broadcast', {'sender': rooms[room]['users'][sid], 'msg': data['msg']}, room=room)

#############
##  Entry  ##
#############

if __name__ == '__main__':
	socketio.run(app)