from base.base import Point


class Renderer():
    def __init__(self, map) -> None:
        self.map = map 
        
    def print_map(self) -> None:
        for x in range(self.map.size):
            for y in range(self.map.size):
                coord = Point(x, y)
                print(self.map.map_dict.get(coord, '⬜️'), end='')
            print("\n")
        print("\n")