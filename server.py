from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from urlgen import urlgen

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret ~'
socketio = SocketIO(app)

suffix_to_sessionid = {}

######################
##  Route Handlers  ##
######################

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/create')
@app.route('/create/')
def show_create():

	# generate url suffix
	suffix = urlgen.generate()

	return redirect(url_for(suffix))

@app.route('/join')
@app.route('/join/')
def show_join():
	return render_template('join.html')


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