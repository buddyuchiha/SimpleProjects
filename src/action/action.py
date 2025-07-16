from random import choice

from base.base import Point
from entities.dynamic import Herbivore, Predator
from entities.static import Grass, Rock, Tree


class Action():
    def __init__(self, map) -> None:
        self.map = map 
        
        dynamic_capacity = int(self.map.size * 0.5)
        static_capacity = int(self.map.size * 0.2)
        
        self.capacity = {
            Rock      : int(dynamic_capacity * 0.2),
            Tree      : int(dynamic_capacity * 0.3),
            Grass     : int(dynamic_capacity * 0.5),
            Herbivore : int(static_capacity * 0.5),
            Predator  : int(static_capacity * 0.5)
        }
                
        self.reset_entities = [
            Grass, Herbivore    
        ]
        
        self.init_actions()
    
    def __random_cord(self, coords) -> int:
        if not coords:
            raise ValueError(coords)
        
        coord = choice(coords)
        coords.remove(coord)
        
        return coord, coords    
    
    def init_actions(self) -> None:
        for x in range(self.map.size):
            coords = [i for i in range(self.map.size)]
            
            for key, value in self.capacity.items():
                for _ in range(value):
                    
                    coord_y, coords = self.__random_cord(coords)
                    point = Point(x, coord_y)
                    self.map.add_entity(point, key)
    
    def reset_action(self) -> None:
        temp_map = self.map.map_dict.copy()
        for reset_entity in self.reset_entities:
            entity_count = self.map.get_entity_count(reset_entity)
            entity_capacity = self.capacity.get(reset_entity) \
            * int(self.map.size / 2)
            
            while entity_count < entity_capacity: 
            
                for x in range(self.map.size):
                    coords = [i for i in range(self.map.size)] 
                    while True:
                        coord_y, coords = self.__random_cord(coords)
                        point = Point(x, coord_y)
                        if not coords: 
                            break
                        
                        if point not in temp_map:
                            self.map.add_entity(point, reset_entity)
                            entity_count += 1
                            break            
                    
    def turn_actions(self) -> None:
        temp_map = self.map.map_dict.copy()
        for key, value in temp_map.items():
            if isinstance(value, Predator):
                self.map.move_creature(key, value)

        temp_map = self.map.map_dict.copy()
        for key, value in temp_map.items():
            if isinstance(value, Herbivore):
                self.map.move_creature(key, value)
            
        self.reset_action()