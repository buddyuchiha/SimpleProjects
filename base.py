from abc import ABC, abstractmethod

class Point():
    def __init__(self, x = None, y = None):
        self.x = x 
        self.y = y
        
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other): 
        return self.x == other.x and self.y == other.y


class Entity(ABC):
    def __init__(self, point: Point, image: str):
        self.image = image 
        self.point = point
        
    def __repr__(self):
        return self.image 
    
    def __str__(self):
        return self.image 

         
    
