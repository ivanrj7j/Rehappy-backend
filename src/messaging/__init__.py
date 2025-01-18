from flask_socketio import SocketIO, join_room, leave_room, emit
from ..models import Community
from ..collections import communityCollection, usersCollection
from flask import request

socket = SocketIO()

@socket.on('connect')
def connectionHandler():
    pass

@socket.on('disconnect')
def disconnectionHandler():
    pass

@socket.on("user_join")
def handleUserJoin(data):
    username = data["username"]
    community = Community(data["community"], communityCollection, usersCollection)
    community.validate()

    if not community.validated:
        print("Invalid Community!")
        emit("invalid_community", {"community": community.name}, to=request.sid)
        # disconnect()
        return
    
    if not community.validateUser(username):
        print("Invalid User!")
        emit("invalid_user", {"user": username}, to=request.sid)
        # disconnect()
        return

    join_room(community)
    print(f"User {username} joined!")
    
    emit("user_connected", {"user": username}, to=community)

@socket.on("message")
def handleSendMessage(data):
    message = data["message"]
    join_room(data["community"])
    user = data["user"]
    emit("chat", {"message": message, "user": user}, to=data["community"])
    