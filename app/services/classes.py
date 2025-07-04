from static.consts import PHRASES



class PlayerClass():
    def __init__(self):
        print (PHRASES.get('begin'))
        self.status = input(f"{PHRASES.get('choice')} ") 
        
    def reset_db(self):
        pass
    
    
    