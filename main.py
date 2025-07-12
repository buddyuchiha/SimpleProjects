from base import Point, Entity, Creature
from dynamic import *
from static import *
from map import *
from actions import *    
    
if __name__ == "__main__":
    map = Map(10)
    create = Action(map)
    map.print_map()
    create.turn_actions()
    map.print_map()