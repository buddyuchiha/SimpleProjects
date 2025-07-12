from base import *
from dynamic import Creature, Predator, Herbivore
class Map():
    def __init__(self, size=None):
        self.size = size
        self.map_dict = {}
        
    def print_map(self) -> None:
        # print(self.map_dict)
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
        # self.print_map()
        # print(f"сработал move_creature для {new_coord} и {obj}")      
        
        
class Simulation():    
    def __init___(self):
        self.map = Map()
        self.counter = 0 