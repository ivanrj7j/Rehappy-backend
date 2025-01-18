class Error(Exception):
    def __init__(self, message:str, *args):
        super().__init__(*args)
        self.message = message

class UserValidationError(Error):
    pass

class CommunityValidationError(Error):
    pass
