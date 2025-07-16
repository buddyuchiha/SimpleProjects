from abc import abstractmethod

from base.base import Point, Entity


class Creature(Entity):
    def __init__(self, point: Point, hp: int, speed: int, image: str) -> None:
        self.hp = hp
        self.speed = speed
        super().__init__(point, image)
        
    def make_move(self, point: Point, path: list[tuple[int, int]]) -> Point:
        if not path:
            return point
            
        speed_path = path[:self.speed]
        new_point = Point(point.x, point.y)
        
        for coords in speed_path:
            new_point.x += coords[0]
            new_point.y += coords[1]
            
        return new_point

class Herbivore(Creature):
    def __init__(
            self, 
            point: Point, 
            hp: int = 10, 
            speed: int = 5, 
            image: str = '🦕'
            ) -> None:
        super().__init__(point, hp, speed, image)
    
    def is_dead(self) -> bool:
        return self.hp <= 0


class Predator(Creature):
    def __init__(
            self, 
            point: Point, 
            damage: int = 5, 
            hp: int = 10, 
            speed: int = 4, 
            image: str = '🦖'
            ) -> None:
        super().__init__(point, hp, speed, image)
        self.damage = damage     
    
    def try_attack(self, target: Herbivore) -> bool:
        if target.is_dead():
            return False
            
        target.hp -= self.damage
        return target.is_dead()