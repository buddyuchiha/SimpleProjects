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

        def change_entity(self, obj: Creature, new_coord: Point, point: Point):
            self.map_dict.pop(point)
            obj.point = new_coord
            self.map_dict[new_coord] = obj
         
        def is_reachable(self,point, obj) -> bool:
            entity = self.map_dict.get(point)
            if isinstance(obj, Herbivore):
                return isinstance(entity, Grass)
            else:
                return isinstance(entity, Herbivore)
                   
        def bfs_shortest_path(
            self, 
            start_point: Point,
            goal_point: Point,
            obj: Entity
            ) -> list[tuple[int, int]]:
            if start_point == goal_point:
                return []

            if not self.is_reachable(goal_point, obj):
                return []

            queue = deque()
            queue.append((start_point, []))
            visited = {start_point: True}  
            

            passable_types = {None, Grass} if isinstance(obj, Herbivore) \
                else {None, Herbivore}
            
            max_depth = self.size * 2
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                current_point, path = queue.popleft()
                
                if len(path) >= max_depth:
                    continue

                for dx, dy in directions:
                    neighbor = Point(current_point.x + dx, current_point.y + dy)
                    
                    if not (0 <= neighbor.x < self.size and \
                        0 <= neighbor.y < self.size):
                        continue
                        
                    if neighbor in visited:
                        continue
                        
                    entity = self.map_dict.get(neighbor)
                    if type(entity) not in passable_types:
                        continue
                        
                    new_path = path + [(dx, dy)]
                    
                    if neighbor == goal_point:
                        print(f"Путь: {new_path}")
                        return new_path
                        
                    visited[neighbor] = True
                    queue.append((neighbor, new_path))
            print("Пусто")
            return [] 
        
        def get_positions(
            self,
            obj: Entity
            ) -> list[Point]:
            positions = [
                point for point, entity in self.map_dict.items() 
                if isinstance(entity, obj)
            ]
            return positions
         
        def get_goal_point(
            self,
            point: Point,
            obj: Entity
            ) -> Point:
            positions = self.get_positions(obj)
            manh_metr = []
            for goal_point in positions:
                manh_metr.append(
                    abs(point.x - goal_point.x) + abs(point.y - goal_point.y)
                    )
            return positions[manh_metr.index(min(manh_metr))]
        
        def get_path(self, point, obj) -> list[tuple[int, int]]:
            goal_point = self.get_goal_point(point, obj)
            return self.bfs_shortest_path(point, goal_point, obj)
        
        def move_creature(self, point: Point, obj: Creature) -> None:
            new_coord = obj.make_move(point, self)
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
                if(isinstance(value, Herbivore)):
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
                        
                
            
        