from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room

from whisper.views import routes
from whisper.common import common

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it\'s a secret ~'
app.register_blueprint(routes)

# TODO: move SocketIO into subpackage
socketio = SocketIO(app)

###############################
##  SocketIO Event Handlers  ##
###############################

@socketio.on('join')
def handle_join(data):
	username = data['username']
	room = data['room']
	if room not in common.rooms:
		return
	session_id = request.sid
	# Map username to user session id in room space
	common.rooms[room]['users'][session_id] = username
	join_room(room)
	print(username + ' joined ' + room)
	send(username + ' has joined the chatroom.', room=room)

@socketio.on('leave')
def handle_leave(data):
	username = data['username']
	room = data['room']
	session_id = request.sid
	leave_room(room)
	print(username + ' left ' + room)
	send(username + ' has left the chatroom.', room=room)
	del common.rooms[room]['users'][session_id]
	# Delete room if all users have left
	if len(common.rooms[room]['users']) == 0:
		print('disposing room ' + room)
		close_room(room)
		del common.rooms[room]
		

@socketio.on('message')
def handle_msg(data):
	room = data['room']
	session_id = request.sid
	# Echo received messages back to room
	emit('broadcast', {
		'sender': common.rooms[room]['users'][session_id],
		'msg': data['msg']
	}, room=room)

#############
##  Entry  ##
#############

if __name__ == '__main__':
	socketio.run(app)