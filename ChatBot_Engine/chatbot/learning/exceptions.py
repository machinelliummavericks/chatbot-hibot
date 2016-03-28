class UserNotImplementedError(NotImplementedError):

    def __init__(self, message="This method must be overridden in a subclass method."):
        self.message = message

    def __str__(self):
        return self.message
