from base import Point, Entity, Creature
from dynamic import *
from static import *
from temp import *
from actions import *    
    
if __name__ == "__main__":
    map = Map(5)
    create = CreateAction(map)
    map.print_map()