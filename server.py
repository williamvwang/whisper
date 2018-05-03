from flask import Flask, render_template, redirect, url_for, abort
from flask_socketio import SocketIO, emit, join_room, leave_room
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
	# Generate url suffix
	suffix = urlgen.generate()
	rooms[suffix] = {
		'id': uuid.uuid4(),
		'suffix': suffix
		'members': []
	}
	return redirect('/' + suffix)

@app.route('/join')
@app.route('/join/')
def show_join():
	return render_template('join.html')

@app.route('/<roomname>')
def enter_room(roomname):
	print(roomname);
	if roomname in rooms:
		return render_template("chatroom.html", room=rooms[roomname])
	else:
		return abort(404)

######################
##  Event Handlers  ##
######################

@socketio.on('connect')
def handle_connect(user):
	emit('response', {'data': 'user connected'})

@socketio.on('disconnect')
def handle_connect(user):
	emit('response', {'data': 'user connected'})

@socketio.on('msg')
def handle_msg(msg):
	emit('response', {'data': 'message received'})


#############
##  Entry  ##
#############

if __name__ == '__main__':
	socketio.run(app)