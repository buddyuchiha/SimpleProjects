from base import *
from static import * 
from dynamic import * 
from map import Map

from random import choice

class CreateAction():
    def __init__(self, map: Map):
        self.map = map 
        
        self.static_capacity = int(self.map.size * 0.5)
        self.dynamic_capacity = int(self.map.size * 0.2)
        
        self.rock_capacity = int(self.static_capacity * 0.2)
        self.tree_capacity = int(self.static_capacity * 0.3)
        self.grass_capacity = round(self.static_capacity * 0.5)
        self.herbivore_capacity = int(self.dynamic_capacity * 0.5)
        self.predator_capacity = int(self.dynamic_capacity * 0.5)

        print(self.map.size)
        print(self.static_capacity, self.dynamic_capacity)   
        print(self.rock_capacity, self.tree_capacity, self.grass_capacity) 
                
        self.__generator()
        
    def __generator(self):
        for x in range(self.map.size):
            self.static_coords = [i for i in range(self.map.size)]
            self.__generate_static(x)
            self.__generate_dynamic(x)
            
    def __random_cord(self) -> int:
        if not self.static_coords:
            raise ValueError(self.static_coords)
        coord = choice(self.static_coords)
        self.static_coords.remove(coord)
        return coord    
    
    def __generate_object(self, x: int, obj_name: str) -> tuple[Entity, int]:
        coord_y = self.__random_cord()
        coord = Point(x, coord_y)
        
        match obj_name:
            case "rock":
                object = Rock(coord) 
            case "tree":
                object = Tree(coord)  
            case "grass":
                object = Grass(coord)  
            case "herbivore":
                object = Herbivore(coord, 10, 1)   
            case "predator":
                object = Predator(coord, 10, 1, 1)  
                
        return object, coord  
    
    def __generate_static(self, x: int) -> None:
        for _ in range(self.rock_capacity):
            obj, obj_coord = self.__generate_object(x, "rock") 
            self.map.map_dict[obj_coord] = obj 
            
        for _ in range(self.tree_capacity):
            obj, obj_coord = self.__generate_object(x, "tree") 
            self.map.map_dict[obj_coord] = obj
            
        for _ in range(self.grass_capacity):
            obj, obj_coord = self.__generate_object(x, "grass") 
            self.map.map_dict[obj_coord] = obj
            
    def __generate_dynamic(self, x: int) -> None:
        for _ in range(self.herbivore_capacity):
            obj, obj_coord = self.__generate_object(x, "herbivore") 
            self.map.map_dict[obj_coord] = obj 
            
        for _ in range(self.predator_capacity):
            obj, obj_coord = self.__generate_object(x, "predator") 
            self.map.map_dict[obj_coord] = obj
              