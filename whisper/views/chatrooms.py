from flask import render_template, redirect, abort
import uuid

from . import routes
from ..urlgen import urlgen
from ..common import common

######################
##  Route Handlers  ##
######################

@routes.route('/')
def index():
	return render_template('index.html')

@routes.route('/create')
@routes.route('/create/')
def create_room():
	# Generate a unique url suffix
	suffix = urlgen.generate()
	while suffix in common.rooms:
		suffix = urlgen.generate()
	# Create an empty room entry for this suffix
	common.rooms[suffix] = {
		'id': uuid.uuid4(),
		'suffix': suffix,
		'users': {}
	}
	return redirect('/' + suffix)

@routes.route('/join')
@routes.route('/join/')
def show_join():
	return render_template('join.html')

@routes.route('/<suffix>')
@routes.route('/<suffix>/')
def enter_room(suffix):
	# Serve room if it exists
	if suffix in common.rooms:
		return render_template("chatroom.html", roomname=suffix)
	else:
		return abort(404)