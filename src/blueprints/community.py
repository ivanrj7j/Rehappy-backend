from flask import Blueprint, request
from ..models import Community
from ..collections import db, usersCollection, communityCollection
from ..misc.exceptions import CommunityValidationError, UserValidationError
from ..misc.utils import loginRequried

communityBluerpint = Blueprint("community", __name__)

@loginRequried
@communityBluerpint.route("/createCommunity", methods=["POST"])
def create_community():
    data = request.get_json()
    admin = data["admin"]
    name = data["name"]

    community = Community(name, communityCollection, usersCollection, db)
    
    community.validate()
    
    try:
        community.create(admin)
        return {"message": "Community created successfully"}, 201
    except CommunityValidationError:
        return {"error": "Community already exists"}, 500
    except UserValidationError:
        return {"error": "User not found"}, 404
    
@loginRequried
@communityBluerpint.route("/joinCommunity", methods=["POST"])
def join_community():
    data = request.get_json()
    user = data["user"]
    name = data["name"]

    community = Community(name, communityCollection, usersCollection, db)
    
    try:
        community.addMember(user)
        return {"message": "User joined community successfully"}, 201
    except CommunityValidationError as e:
        return {"error": str(e)}, 404
    except UserValidationError as e:
        return {"error": str(e)}, 500
    
@loginRequried
@communityBluerpint.route("/leaveCommunity", methods=["POST"])
def leave_community():
    data = request.get_json()
    user = data["user"]
    name = data["name"]

    community = Community(name, communityCollection, usersCollection, db)
    
    try:
        community.removeMember(user)
        return {"message": "User left community successfully"}, 200
    except CommunityValidationError as e:
        return {"error": str(e)}, 404
    except UserValidationError as e:
        return {"error": str(e)}, 500