class ValidationError(Exception):
    def __init__(self, message:str, *args):
        super().__init__(*args)
        self.message = message