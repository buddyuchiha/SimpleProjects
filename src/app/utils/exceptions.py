class ServerError500(Exception):
    def __init__(self, message: str = "Internal Server Error"):
        self.message = message
        super().__init__(self.message)
        
        
class BadRequest400(Exception):
    def __init__(self, message: str = "Bad Request"):
        self.message = message
        super().__init__(self.message)
    
    
class NotFound404(Exception):
    def __init__(self, message: str = "Not Found"):
        self.message = message
        super().__init__(self.message)  


class Conflict409(Exception):
    def __init__(self, message: str = "Conflict"):
        self.message = message
        super().__init__(self.message)    