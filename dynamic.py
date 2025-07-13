from abc import ABC, abstractmethod
from collections import deque

from base import Point, Entity
from static import Grass

class Creature(Entity):
    def __init__(self, point: Point, hp: int, speed: int, image: str):
        self.hp = hp
        self.speed = speed
        super().__init__(point, image)
        
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
            point: Point,
            map
            ) -> Point: 
        path = map.get_path(point, Herbivore)
        speed_path = path[:self.speed]
        
        if (len(path) == 1):
            goal_point = map.get_goal_point(point, Herbivore)
            herbivore = map.map_dict.get(goal_point)
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