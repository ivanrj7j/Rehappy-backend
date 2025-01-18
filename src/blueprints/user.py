from flask import Blueprint
from flask import session
from flask import request
# importing flask related stuff 


from ..models import User
# importing models 

from ..collections import usersCollection
# collections 

from ..misc.exceptions import ValidationError
from ..misc.utils import loginRequried, noLoginRequried
# misc


userBlueprint = Blueprint("user", __name__)



@noLoginRequried
@userBlueprint.route('/register', methods=['POST'])
def createUser():
    data = request.get_json()

    username = data['username']
    password = data['password']

    user = User(username, usersCollection)

    try:
        user.register(password)
        session['username'] = username
        return {"message": "User created successfully"}, 201
    except ValidationError:
        return {"message": "Invalid username or password"}, 400
    
@noLoginRequried
@userBlueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    user = User(username, usersCollection)

    try:
        user.login(password)
        session['username'] = username

        return {"message": "User logged in successfully"}, 200
    
    except ValidationError:
        return {"message": "Invalid username or password"}, 401
    
@loginRequried
@userBlueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)

    return {"message": "User logged out successfully"}, 200

@loginRequried
@userBlueprint.route('/deleteUser', methods=['PUT'])
def deleteuser():
    username = session['username']

    user = User(username, usersCollection)
    try:
        user.deleteUser()
        return {"message": "User deleted successfully"}, 200
    except ValidationError:
        return {"message": "Invalid username"}, 400
    
@loginRequried
@userBlueprint.route('/updateUser', methods=['PUT'])
def updateUser():
    data = request.get_json()
    username = session['username']
    oldPassword = data['oldPassword']

    newPassword = data["newPassword"]

    user = User(username, usersCollection)
    try:
        user.changePassword(oldPassword, newPassword)
        return {"message": "User password updated successfully"}, 200
    except ValidationError:
        return {"message": "Invalid username or password"}, 400