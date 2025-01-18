from pymongo.collection import Collection
from ..misc import ValidationError

class User:
    def __init__(self, username:str, collection:Collection):
        self.username = username
        self.collection = collection
        self.validated = False

    def validate(self):
        check = self.collection.find_one({
            "username": self.username
        })
        
        self.validated = check is not None

    def validationCheck(self):
        if not self.validated:
            raise ValidationError("The user is not validated")
        
    def register(self, password:str) -> bool:
        self.validate()
        # validating the user 

        if self.validated:
            raise ValidationError("The user is already registered")
        
        result = self.collection.insert_one({
            "username": self.username,
            "password": password
        })

        self.validated = result.acknowledged

        return result.acknowledged

    def login(self, password:str) -> bool:
        check = self.collection.find_one({
            "username": self.username,
            "password": password
        })

        if check is None:
            raise ValidationError("The username and passwords do not match")
        
        self.validated = True

    def deleteUser(self):
        if not self.validated:
            raise ValidationError("The user is not validated")
        
        self.collection.delete_one({
            "username": self.username
        })

    def changePassword(self, oldPassword:str, newPassword:str) -> bool:
        if not self.validated:
            raise ValidationError("The user is not validated")
        
        update = self.collection.update_one({
            "username": self.username,
            "password": oldPassword
        }, {
            "$set": {
                "password": newPassword
            }
        })

        if update.modified_count > 0:
            return True
        
        raise ValidationError("The old password and username combination is incorrect")