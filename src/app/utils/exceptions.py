class RequestException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ServerError500(RequestException):
    def __init__(self, message: str = "Internal Server Error"):
        super().__init__(message)
        
        
class BadRequest400(RequestException):
    def __init__(self, message: str = "Bad Request"):
        super().__init__(message)
    
    
class NotFound404(RequestException):
    def __init__(self, message: str = "Not Found"):
        super().__init__(message)  


class Conflict409(RequestException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message)    