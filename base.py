from abc import ABC, abstractmethod

class Point():
    def __init__(self, x , y):
        self.x = x 
        self.y = y
        
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other): 
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    # def get_neighbours(self, size: int):
    #     coords = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    #     neighbors = []
    #     for dx, dy in coords:
    #         neighbor = Point(self.x + dx, self.y + dy)
    #         if not (0 <= neighbor.x < size and 0 <= neighbor.y < size):
    #             neighbors.append(neighbor)
    #     return neighbors


class Entity(ABC):
    def __init__(self, point: Point, image: str):
        self.image = image 
        self.point = point
        
    def __repr__(self):
        return self.image 
    
    def __str__(self):
        return self.image 

         
    
