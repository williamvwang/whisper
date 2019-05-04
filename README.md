# whisper

*portable private conversations*

built with [Flask-SocketIO](https://flask-socketio.readthedocs.io).

## Local project setup
Project dependencies are listed in `requirements.txt`. To install, simply run:

```bash
pip install -r requirements.txt
```
Then to start the Flask server:

```bash
export FLASK_APP=server.py
flask run
```

## Usage

Create a new chatroom by navigating to `/create`. This generates a room with a unique three-word identifier in the Adjective-Adjective-Noun pattern, which can be shared with others wishing to join the chatroom.

Join a chatroom by navigating to `/<identifier>`, where `<idenfitier>` is the unique three-word identifier of an extant room.
