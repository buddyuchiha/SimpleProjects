from base import Creature, Point


class Herbivore(Creature):
    def __init__(self, 
                 point: Point, 
                 hp: int = 10, 
                 speed: int = 1, 
                 image: str = '🦕'
                 ):
        super().__init__(point, hp, speed, image)
        
    def make_move(self):
        pass


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
        
    def make_move(self):
        pass