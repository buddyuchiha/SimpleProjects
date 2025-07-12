from random import choice

from base import Entity, Point
from dynamic import Creature, Herbivore, Predator
from static import Grass, Rock, Tree


class Simulation():
    def __init__(self):
        map = self.Map(10)
        action = self.Action(map)
        map.print_map()
        action.turn_actions()
        map.print_map() 
        
    
    class Map():
        def __init__(self, size=None):
            self.size = size
            self.map_dict = {}
            
        def print_map(self) -> None:
            for x in range(self.size):
                for y in range(self.size):
                    coord = Point(x, y)
                    print(self.map_dict.get(coord, '⬜️'), end='')
                print("\n")
            print("\n")
                
        def add_entity(self, point: Point, obj: Entity) -> None:
            map_obj = obj(point)
            self.map_dict[point] = map_obj 

        def move_creature(self, point: Point, obj: Creature) -> None:
            new_coord = obj.make_move(self.map_dict, point, self.size, obj)
            if (isinstance(obj, Predator)):
                target = self.map_dict.get(new_coord)
                if(isinstance(target, Herbivore)):
                    if (target.get_hp() == 0):
                        self.map_dict.pop(point)
                        obj.point = new_coord
                        self.map_dict[new_coord] = obj
                        print(f"{target} убит")
                    else:
                        print(f"{target} ранен")
                else:
                    self.map_dict.pop(point)
                    obj.point = new_coord
                    self.map_dict[new_coord] = obj
            else:
                self.map_dict.pop(point)
                obj.point = new_coord
                self.map_dict[new_coord] = obj
    
    class Action():
        def __init__(self, map):
            self.map = map 
            self.capacity = {
                Rock      : int(self.map.size * 0.5 * 0.2),
                Tree      : int(self.map.size * 0.5 * 0.3),
                Grass     : int(self.map.size * 0.5 * 0.5),
                Herbivore : int(self.map.size * 0.2 * 0.5),
                Predator  : int(self.map.size * 0.2 * 0.5)
            }
                    
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
            
        