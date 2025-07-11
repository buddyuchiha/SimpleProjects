from base import Creature, Point, Entity
from static import Grass
from map import Map

class Herbivore(Creature):
    def __init__(self, 
                 point: Point, 
                 hp: int = 10, 
                 speed: int = 1, 
                 image: str = '🦕'
                 ):
        super().__init__(point, hp, speed, image)
        
    def make_move(self, map_dict: dict[Point, Entity], point: Point, size: int):
        grass_positions = [
            point for point, entity in map_dict.items() 
            if isinstance(entity, Grass)
        ]
        
        if not grass_positions:
            pass 
        
        manh_metr = []
        for grass_point in grass_positions:
            manh_metr.append(
                abs(point.x - grass_point.x) + abs(point.y - grass_point.y))
            
        goal = grass_positions[manh_metr.index(min(manh_metr))]
        
                  


class Predator(Creature):
    def __init__(self, 
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