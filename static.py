from base import Point, Entity


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
