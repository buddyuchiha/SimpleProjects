from base import Point, Entity
class Map():
    def __init__(self, size=None):
        self.size = size
        self.map_dict = {}
        # for i in range(size):
        #     point = Point()
        #     self.map[point] = ['q']
        # print(self.map)
        
    def print_map(self) -> None:
        print(self.map_dict)
        for x in range(self.size):
            for y in range(self.size):
                coord = Point(x, y)
                print(self.map_dict.get(coord, '⬜️'), end='')
            print("\n")
            
    def add_entity(self, point: Point, obj: Entity) -> None:
        map_obj = obj(point)
        self.map_dict[point] = map_obj 


class Simulation():    
    def __init___(self):
        self.map = Map()
        self.counter = 0 