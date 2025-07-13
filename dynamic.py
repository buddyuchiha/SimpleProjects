from abc import ABC, abstractmethod
from collections import deque

from base import Point, Entity
from static import Grass

class Creature(Entity):
    def __init__(self, point: Point, hp: int, speed: int, image: str):
        self.hp = hp
        self.speed = speed
        super().__init__(point, image)
        
    def get_positions(self, map_dict: dict[Point, Entity], obj: Entity):
        positions = [
            point for point, entity in map_dict.items() 
            if isinstance(entity, obj)
        ]
        return positions
    
    def get_goal_point(self, point, positions):
        manh_metr = []
        for goal_point in positions:
            manh_metr.append(
                abs(point.x - goal_point.x) + abs(point.y - goal_point.y)
                )
        return positions[manh_metr.index(min(manh_metr))]
    
    def bfs_shortest_path(
                self, 
                map_dict: dict[Point, Entity],
                start_point: Point,
                goal_point: Point,
                size: int,
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

            coords = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            while queue:
                current_point, path = queue.popleft()

                if current_point == goal_point:
                    print(f"Path from {start_point} to {goal_point}: {path}")
                    return path

                for dx, dy in coords:
                    neighbor = Point(current_point.x + dx, current_point.y + dy)

                    if not (0 <= neighbor.x < size and 0 <= neighbor.y < size):
                        continue
                        
                    if neighbor not in visited:
                        entity = map_dict.get(neighbor)
                        if entity is None or isinstance(entity, entity_type):
                            visited.add(neighbor)
                            queue.append((neighbor, path + [(dx, dy)]))

            return []
    
    @abstractmethod
    def make_move(self) -> Point:
        pass 
    

class Herbivore(Creature):
    def __init__(
            self, 
            point: Point, 
            hp: int = 10, 
            speed: int = 5, 
            image: str = '🦕'
            ):
        super().__init__(point, hp, speed, image)
    
    def is_dead(self):
        return self.hp == 0
    
    def make_move(
            self,
            map_dict: dict[Point, Entity],
            point: Point,
            map_size: int,
            obj: Entity
            ) -> Point:
        grass_positions = self.get_positions(map_dict, Grass)

        if not grass_positions:
            return Point(point.x, point.y)
        
        goal_point = self.get_goal_point(point, grass_positions)

        path = self.bfs_shortest_path(
            map_dict, point, goal_point, map_size, obj
            )  
         
        speed_path = path[:self.speed]
        
        new_point = Point(point.x, point.y)
        for coords in speed_path:
            new_point.x += coords[0]
            new_point.y += coords[1]

        return new_point
    
    def get_hp(self) -> int:
        return self.hp


class Predator(Creature):
    def __init__(
            self, 
            point: Point, 
            damage: int = 5, 
            hp: int = 10, 
            speed: int = 4, 
            image: str = '🦖'
            ):
        super().__init__(point, hp, speed, image)
        self.damage = damage     
        
    def make_move(
            self,
            map_dict: dict[Point, Entity],
            point: Point,
            map_size: int,
            obj: Entity
            ) -> Point:
        herbivore_positions = self.get_positions(map_dict, Herbivore)
        # herbivore_positions = [
        #     point for point, entity in map_dict.items() 
        #     if isinstance(entity, Herbivore)
        # ]
        # print("ход хищника")
        if not herbivore_positions:
            print("Нет позиций")
            return Point(point.x, point.y)
        
        goal_point = self.get_goal_point(point, herbivore_positions)
        # manh_metr = []
        # for herbivore_point in herbivore_positions:
        #     manh_metr.append(
        #         abs(point.x - herbivore_point.x) + abs(point.y - herbivore_point.y)
        #         )
            
        # goal_point = herbivore_positions[manh_metr.index(min(manh_metr))]
        path = self.bfs_shortest_path(
            map_dict, point, goal_point, map_size, obj
            )  
         
        speed_path = path[:self.speed]
        
        if (len(path) == 1):
            herbivore = map_dict.get(goal_point)
            herbivore.hp -= self.damage
            if herbivore.is_dead():
                return goal_point
            else:
                # print("Охотник двинулся")
                return point
        if (len(speed_path) == len(path)):
            speed_path = path[:self.speed+1]
            
            
        new_point = Point(point.x, point.y)
        for coords in speed_path:
            new_point.x += coords[0]
            new_point.y += coords[1]

        # print("Охотник двинулся")
        return new_point
    
    def attack_creature(self, obj, map_dict, goal_point):
        obj = map_dict.get()