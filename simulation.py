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
        for _ in range(10):
            action.turn_actions()
            map.print_map() 
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
        
        def del_entity(self, point: Point) -> None: 
            self.map_dict.pop(point)
                
        def add_entity(self, point: Point, obj: Entity) -> None:
            map_obj = obj(point)
            self.map_dict[point] = map_obj 

        def move_entity(self, point: Point, obj: Creature, goal_point):
            self.del_entity(point)
            obj.point = goal_point
            self.map_dict[goal_point] = obj
         
        def get_object(self, obj):
            if isinstance(obj, Herbivore):
                obj = Grass
            elif isinstance(obj, Predator):
                obj = Herbivore
            return obj
         
        def is_reachable(self, point: Point, obj: Creature) -> bool:
            entity = self.map_dict.get(point)
            
            if isinstance(entity, Rock):
                return False
                
            if isinstance(obj, Herbivore):
                return entity is None or isinstance(entity, Grass)
            
            elif isinstance(obj, Predator):
                return entity is None or isinstance(entity, Herbivore)
            
            return False

        def bfs_shortest_path(self, start_point: Point, goal_point: Point, obj: Entity) -> list[tuple[int, int]]:
            queue = deque([(start_point, [])])
            visited = set([start_point])
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                current_point, path = queue.popleft()

                if current_point == goal_point:
                    return path

                for dx, dy in directions:
                    neighbor = Point(current_point.x + dx, current_point.y + dy)

                    if not (0 <= neighbor.x < self.size and 0 <= neighbor.y < self.size):
                        continue

                    if neighbor not in visited:
                        entity = self.map_dict.get(neighbor)
                        
                        if entity is None or (neighbor == goal_point and self.is_reachable(neighbor, obj)):
                            visited.add(neighbor)
                            queue.append((neighbor, path + [(dx, dy)]))
                        else:
                            visited.add(neighbor)  
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
            obj = self.get_object(obj)    
            positions = self.get_positions(obj)
            
            if not positions: 
                return [] 
            
            manh_metr = []
            for goal_point in positions:
                manh_metr.append(
                    abs(point.x - goal_point.x) + abs(point.y - goal_point.y)
                    )
            return positions[manh_metr.index(min(manh_metr))]
        
        def move_predator(self, point: Point, obj: Predator, path, new_coord):
            goal = self.get_goal_point(point, obj)
            
            if (len(path) == 1):
                target = self.map_dict.get(goal)
                print(f"Существо по координате: {target} x {goal.x} y {goal.y}")
                
                if isinstance(target, Herbivore) and obj.try_attack(target):
                    print (f"{target} убит x {goal.x} y {goal.y}")
                    self.move_entity(point, obj, goal)   
                else:
                    print(f"target:{target}")
                    self.move_entity(point, obj, goal)  
            else: 
                self.move_entity(point, obj, new_coord)
                
        def move_herbivore(self, point, obj, new_coord):
            self.move_entity(point, obj, new_coord)
        
        def move_creature(self, point: Point, obj: Creature) -> None:
            goal = self.get_goal_point(point, obj) 
            path = self.bfs_shortest_path(point, goal, obj)
            new_coord = obj.make_move(point, path)
            
            print(f"Старая координата: {point} {point.x} {point.y}")
            print(f"Координата: {new_coord} {new_coord.x} {new_coord.y}")
            print(f"Путь: {path}")
            
            if isinstance(obj, Predator):
                self.move_predator(point, obj, path, new_coord)
            elif isinstance(obj, Grass):
                self.move_herbivore(point, obj, new_coord)

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
                if(isinstance(value, Creature)):
                    self.map.move_creature(key, value)
                                        