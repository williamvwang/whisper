from flask import Flask, render_template, redirect, abort, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from whisper.routing import routes
from whisper.common import common

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it\'s a secret ~'
app.register_blueprint(routes)

socketio = SocketIO(app)

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
	if room not in common.rooms:
		return
	sid = request.sid
	# Map username to session id in room space
	common.rooms[room]['users'][sid] = username
	join_room(room)
	send(username + ' has entered the chatroom.', room=room)

@socketio.on('leave')
def handle_leave(data):
	# Extract username, room, and session id
	username = data['username']
	room = data['room']
	sid = request.sid
	leave_room(room)
	send(username + ' has left the chatroom.', room=room)
	del common.rooms[room]['users'][sid]
	# Delete room if all users have left
	if len(common.rooms[room]['users'] == 0):
		del common.rooms[room]

@socketio.on('message')
def handle_msg(data):
	room = data['room']
	sid = request.sid
	# Echo received messages back to room
	emit('broadcast', {'sender': common.rooms[room]['users'][sid], 'msg': data['msg']}, room=room)

#############
##  Entry  ##
#############

if __name__ == '__main__':
	socketio.run(app)