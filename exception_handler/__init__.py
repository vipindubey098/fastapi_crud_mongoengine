class CustomExceptionHandler(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        s = str(self.code) + ":" + self.message