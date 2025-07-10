from base import *
from static import * 
from dynamic import * 
from temp import Map

from random import choice

class CreateAction():
    def __init__(self, map: Map):
        self.map = map 
        self.coords = [i for i in range(self.map.size)] * 5
        self.static_capacity = int(self.map.size * 0.5)
        self.dynamic_capacity = int(self.map.size * 0.2)
        self.__generator()
        print(self.coords)
        print(self.map.size)
        print(self.static_capacity, self.dynamic_capacity)   
        
    def __generator(self):
        for x in range(self.map.size):
            obj, obj_coord = self.__generate_static(x) 
            self.map.map_dict[obj_coord] = obj
            
    def __random_cord(self) -> int:
        coord = choice(self.coords)
        self.coords.remove(coord)
        return coord    
     
    def __generate_static(self, x: int):
        counter = 0
        while counter != self.static_capacity:
            coord_y = self.__random_cord()
            point = Point(x, coord_y)
            coord = hash(point)
            rock = Rock(coord)
            counter += 1
        return rock, coord  
            
    def __generate_dynamic(self):
        pass          
