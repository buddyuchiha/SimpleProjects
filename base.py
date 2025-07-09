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


class Creature(Entity):
    def __init__(self, point: Point, hp: int, speed: int, image: str):
        self.hp = hp
        self.speed = speed
        super().__init__(point, image)
        
    @abstractmethod    
    def make_move(self):
        pass 
         
    
class Map():
    def __init__(self, size=None):
        self.size = size
        self.map = {}
        # for i in range(size):
        #     point = Point()
        #     self.map[point] = ['q']
        # print(self.map)
        
    def print_map(self) -> None:
        for x in range(self.size):
            for y in range(self.size):
                p = Point(x, y)
                if self.map.get(p): 
                    print(self.map.get(p), end = '')                    
                else:
                    print('-', end = '')
            print(" ")
            
    def add_grass(self):
        for x in range(self.size):
            for y in range(self.size):
                pass 


class Simulation():    
    def __init___(self):
        pass 
    
    

map = Map(5)
map.print_map()

# class Point, словарь объектов