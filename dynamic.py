from collections import deque

from base import Creature, Point, Entity
from static import Grass
from map import Map

class Herbivore(Creature):
    def __init__(
            self, 
            point: Point, 
            hp: int = 10, 
            speed: int = 5, 
            image: str = '🦕'
            ):
        super().__init__(point, hp, speed, image)
          
    def bfs_shortest_path(
            self, 
            map_dict: dict[Point, Entity],
            start_point: Point,
            goal_point: Point,
            size: int
            ) -> list[tuple[int, int]]:
        queue = deque()
        queue.append((start_point, []))
        visited = set()
        visited.add(start_point)  

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
                    if entity is None or isinstance(entity, Grass):
                        visited.add(neighbor)
                        queue.append((neighbor, path + [(dx, dy)]))

        return []
    
    def make_move(
            self,
            map_dict: dict[Point, Entity],
            point: Point,
            map_size: int
            ):
        grass_positions = [
            point for point, entity in map_dict.items() 
            if isinstance(entity, Grass)
        ]
        
        if not grass_positions:
            return Point 
        
        manh_metr = []
        for grass_point in grass_positions:
            manh_metr.append(
                abs(point.x - grass_point.x) + abs(point.y - grass_point.y)
                )
            
        goal_point = grass_positions[manh_metr.index(min(manh_metr))]
        path = self.bfs_shortest_path(
            map_dict, point, goal_point, map_size
            )  
         
        path = path[:self.speed]
        
        new_point = Point(point.x, point.y)
        for coords in path:
            new_point.x += coords[0]
            new_point.y += coords[1]

        return new_point


class Predator(Creature):
    def __init__(
            self, 
            point: Point, 
            damage: int = 2, 
            hp: int = 10, 
            speed: int = 2, 
            image: str = '🦖'
            ):
        super().__init__(point, hp, speed, image)
        self.damage = damage     
        
    def make_move(self, map_dict: dict[Point, Entity], point: Point) -> Point:
        pass