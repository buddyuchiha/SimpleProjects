from abc import ABC, abstractmethod
from collections import deque

from base import Point, Entity
from static import Grass

class Creature(Entity):
    def __init__(self, point: Point, hp: int, speed: int, image: str):
        self.hp = hp
        self.speed = speed
        super().__init__(point, image)
        
    def make_move(
        self,
        point: Point,
        path
        ) -> list[tuple[int, int]]:   
        print("MAKE MOVE") 
        if not path:
            print(f"{path}")
            return point
        
        speed_path = path[:self.speed]
        new_point = Point(point.x, point.y)
        
        for coords in speed_path:
            new_point.x += coords[0]
            new_point.y += coords[1]
            
        print(f"{new_point}")
        return new_point
    

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
        return self.hp <= 0
    
    def make_move(
            self,
            point: Point,
            path
            ) -> list[tuple[int, int]]:   
        if not path:
            print(f"{path}")
            return point
        
        speed_path = path[:self.speed]
        new_point = Point(point.x, point.y)
        
        for coords in speed_path:
            new_point.x += coords[0]
            new_point.y += coords[1]
            
        print(f"Схавал {new_point}")
        return new_point


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
        
    def make_move(self, point: Point, path) -> Point:
        if not path:
            return point
            
        if len(path) == 1:
            return point
            
        speed_path = path[:self.speed]
        new_point = Point(point.x, point.y)
        
        for coords in speed_path:
            new_point.x += coords[0]
            new_point.y += coords[1]
            
        return new_point
    
    def try_attack(self, target: Herbivore) -> bool:
        target.hp -= self.damage
        print(f"🦖 атакует 🦕 на {target.point.x}, {target.point.y}. Осталось HP: {target.hp}")
        return target.is_dead()