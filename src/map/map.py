from collections import deque

from base.base import Entity, Point
from entities.dynamic import Creature, Herbivore, Predator
from entities.static import Grass, Rock


class Map():
    def __init__(self, size=None) -> None:
        self.size = size
        self.map_dict = {}
    
    def del_entity(self, point: Point) -> None: 
        del self.map_dict[point]
            
    def add_entity(self, point: Point, obj: Entity) -> None:
        map_obj = obj(point)
        self.map_dict[point] = map_obj 

    def move_entity(
        self,
        point: Point,
        obj: Creature,
        goal_point: Point
        ) -> None:
        self.del_entity(point)
        obj.point = goal_point
        self.map_dict[goal_point] = obj
        
    def get_entity(self, point: Point) -> bool:
        return self.map_dict.get(point)
        
    @staticmethod
    def get_object(obj: Herbivore | Predator) -> Grass | Herbivore:
        if isinstance(obj, Herbivore):
            obj = Grass
            
        elif isinstance(obj, Predator):
            obj = Herbivore
            
        return obj
        
    def get_entity_count(self, obj: Entity) -> int:
        objects = [
            value for value in self.map_dict.values() 
            if isinstance(value, obj)
            ]     
        return len(objects)
        
    def is_reachable(self, point: Point, obj: Creature) -> bool:
        entity = self.map_dict.get(point)
        
        if isinstance(entity, Rock):
            return False
            
        if isinstance(obj, Herbivore):
            return entity is None or isinstance(entity, Grass)
        
        elif isinstance(obj, Predator):
            return entity is None or isinstance(entity, Herbivore)
        
        return False

    def bfs_shortest_path(
        self,
        start_point: Point,
        goal_point: Point,
        obj: Entity
        ) -> list[tuple[int, int]]:
        queue = deque([(start_point, [])])
        visited = set([start_point])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            current_point, path = queue.popleft()

            if current_point == goal_point:
                return path

            for dx, dy in directions:
                neighbor = Point(
                    current_point.x + dx, 
                    current_point.y + dy
                    )

                if not (0 <= neighbor.x < self.size \
                    and 0 <= neighbor.y < self.size):
                    continue

                if neighbor not in visited:
                    entity = self.map_dict.get(neighbor)
                    
                    if entity is None or (neighbor == goal_point \
                        and self.is_reachable(neighbor, obj)):
                        visited.add(neighbor)
                        queue.append((neighbor, path + [(dx, dy)]))
                        
                    else:
                        visited.add(neighbor)  
        return []  
            
    def get_positions(self, obj: Entity) -> list[Point]:
        positions = [
            point for point, entity in self.map_dict.items() 
            if isinstance(entity, obj)
        ]
        return positions
        
    def get_goal_point(self, point: Point, obj: Entity) -> Point:
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
    
    def move_predator(self, point: Point, obj: Predator) -> None:
        goal = self.get_goal_point(point, obj)
        if not goal:
            return
        
        target = self.map_dict.get(goal)
        if not target or not isinstance(target, Herbivore):
            return
        
        path = self.bfs_shortest_path(point, goal, obj)
        
        if len(path) == 1:
            if obj.try_attack(target):
                self.del_entity(goal)
                if goal not in self.map_dict:
                    self.move_entity(point, obj, goal)
        else:
            new_coord = obj.make_move(point, path)
            if self.map_dict.get(new_coord) != Predator:
                self.move_entity(point, obj, new_coord)
            
    def move_herbivore(self, point: Point, obj: Herbivore) -> None:
        goal = self.get_goal_point(point, obj) 
        path = self.bfs_shortest_path(point, goal, obj)
        new_coord = obj.make_move(point, path)
        
        self.move_entity(point, obj, new_coord)
    
    def move_creature(self, point: Point, obj: Creature) -> None:
        if isinstance(obj, Herbivore):
            self.move_herbivore(point, obj)
        
        elif isinstance(obj, Predator):
            self.move_predator(point, obj)