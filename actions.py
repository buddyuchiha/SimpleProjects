from base import *
from static import * 
from dynamic import * 
from map import Map

from random import choice

class Action():
    def __init__(self, map: Map):
        self.map = map 
        self.capacity = {
            Rock      : int(self.map.size * 0.5 * 0.2),
            Tree      : int(self.map.size * 0.5 * 0.3),
            Grass     : int(self.map.size * 0.5 * 0.5),
            Herbivore : int(self.map.size * 0.2 * 0.5),
            Predator  : int(self.map.size * 0.2 * 0.5)
        }

        print(self.map.size)
                
        self.init_actions()
    
    def __random_cord(self) -> int:
        if not self.coords:
            raise ValueError(self.coords)
        
        coord = choice(self.coords)
        self.coords.remove(coord)
        
        return coord    
    
    def init_actions(self) -> None:
        for x in range(self.map.size):
            self.coords = [i for i in range(self.map.size)]
            for key, value in self.capacity.items():
                for _ in range(value):
                    coord_y = self.__random_cord()
                    point = Point(x, coord_y)
                    self.map.add_entity(point, key)
                    
    def turn_actions(self) -> None:
        temp_map = self.map.map_dict.copy()
        for key, value in temp_map.items():
            if(isinstance(value, Creature)):
                self.map.move_creature(key, value)
        
                