from base import Entity, Point

class Grass(Entity):
    def __init__(self,
                 point: Point,
                 image: str = "🌱"
                 ):
        super().__init__(point, image)


class Rock(Entity): 
    def __init__(self,
                 point: Point,
                 image: str = "🗿"
                 ):
        super().__init__(point, image)


class Tree(Entity):
    def __init__(self,
                 point: Point,
                 image: str = "🌳"
                 ):
        super().__init__(point, image)
