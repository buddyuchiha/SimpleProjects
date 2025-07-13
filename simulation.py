from collections import deque
from random import choice

from base import Entity, Point
from dynamic import Creature, Herbivore, Predator
from static import Grass, Rock, Tree


class Simulation():
    def __init__(self):
        map = self.Map(10)
        action = self.Action(map)
        map.print_map()
        for i in range(10):
            action.turn_actions()
        map.print_map() 
        print(map.map_dict)
        print(action.capacity)
        
    def next_turn(self):
        pass 
    
    def start_simulation(self):
        pass 
    
    def pause_simulation(self):
        pass
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

        def change_entity(
            self,
            obj: Creature, 
            new_coord: Point,
            point: Point
            ):
            self.map_dict.pop(point)
            obj.point = new_coord
            self.map_dict[new_coord] = obj
            
        def bfs_shortest_path(
            self, 
            start_point: Point,
            goal_point: Point,
            obj: Entity
            ) -> list[tuple[int, int]]:
            queue = deque()
            queue.append((start_point, []))
            visited = set()
            visited.add(start_point)  
            
            if(isinstance(obj, Herbivore)):
                entity_type = Grass 
            elif(isinstance(obj, Predator)):
                entity_type = Herbivore

            while queue:
                current_point, path = queue.popleft()

                if current_point == goal_point:
                    # print(f"Path from {start_point} to {goal_point}: {path}")
                    return path

                neighbors = current_point.get_neighbours(self.size)
                    
                for neighbor in neighbors:        
                    if neighbor not in visited:
                        entity = self.map_dict.get(neighbor)
                        if entity is None or isinstance(entity, entity_type):
                            visited.add(neighbor)
                            queue.append((neighbor, path + [(neighbor.x, neighbor.y)]))

            return []
        
        def move_creature(self, point: Point, obj: Creature) -> None:
            new_coord = obj.make_move(self.map_dict, point, self.size, obj)
            if (isinstance(obj, Predator)):
                target = self.map_dict.get(new_coord)
                if(isinstance(target, Herbivore)):
                    if target.is_dead():
                        self.change_entity(obj, new_coord, point)
                        # self.map_dict.pop(point)
                        # obj.point = new_coord
                        # self.map_dict[new_coord] = obj
                        print(f"{target} убит")
                    # else:
                    #     print(f"{target} ранен")
                else:
                    self.change_entity(obj, new_coord, point)
            else:
                self.change_entity(obj, new_coord, point)
    
    class Action():
        def __init__(self, map):
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
                # print("перебор")
                if(isinstance(value, Creature)):
                    self.map.move_creature(key, value)
                    # print("добавлен чел")
                                        
                                        
            # for value in self.map.map_dict.values():
            #     if isinstance(value, Grass):
            #         grass_count += 1
            #     if isinstance(value, Herbivore):
            #         herbivore_count += 1
                              
            # self.coords = [i for i in range(self.map.size)]
            # for i in self.reset_entities:
            #     entity = self.map.map_dict.get(i)
            #     capacity = self.capacity.get(i)
            #     if capacity < grass_count:
            #         for x in range(self.map.size):
            #             pass 
                        
                
            
        