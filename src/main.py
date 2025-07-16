from action.action import Action
from map.map import Map
from renderer.renderer import Renderer

from simulation.simulation import Simulation
    
if __name__ == "__main__":
    map = Map(10)
    renderer = Renderer(map)
    action = Action(map)
    
    sim = Simulation(map, renderer, action)