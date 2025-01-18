from pymongo.collection import Collection
from pymongo.database import Database
from ..misc.exceptions import CommunityValidationError, UserValidationError
from .user import User
import time
from uuid import uuid4

class Community:
    def __init__(self, name:str, community:Collection, users:Collection, db:Database):
        self.name = name
        self.community = community
        self.users = users
        self.messages = db[name]
        self.validated = False

    def validate(self):
        check = self.community.find_one({
            "name": self.name
        })

        self.validated = check is not None

    def validationCheck(self):
        if not self.validated:
            CommunityValidationError("The community is not validated")

    def create(self, admin:str):
        user = User(admin, self.users)

        user.validate()
        user.validationCheck()

        self.validate()
        if self.validated:
            raise CommunityValidationError("Community already exists")

        community = {
            "name": self.name,
            "admin": admin,
            "members": [admin],
        }

        self.community.insert_one(community)
        self.validated = True

    def addMember(self, userName:str):
        self.validationCheck()

        user = User(userName, self.users)
        user.validate()
        user.validationCheck()


        check = self.community.find_one({
            "name": self.name,
            "members": {
                "$in": [userName]
            }
        })

        if check is not None:
            raise UserValidationError("User exists in the community")
        
        self.community.update_one({
            "name": self.name
        }, {
            "$push": {
                "members": userName
            }
        })

    def removeMember(self, userName:str):
        self.validationCheck()

        user = User(userName, self.users)
        user.validate()
        user.validationCheck()

        self.community.update_one({
            "name": self.name
        }, {
            "$pull": {
                "members": userName
            }
        })

    @property
    def memberCount(self):
        self.validationCheck()

        return self.community.find_one({"name": self.name})["members"].count()
    
    def sendMessage(self, sender:str, message:str):
        self.validationCheck()

        user = User(sender, self.users)
        user.validate()
        user.validationCheck()

        self.messages.insert_one({
            "sender": sender,
            "message": message,
            "timestamp": time.time(),
            "id": str(uuid4())
        })
    
