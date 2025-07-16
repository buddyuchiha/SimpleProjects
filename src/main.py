from simulation.simulation import Simulation, Map, Renderer, Action
    
if __name__ == "__main__":
    map = Map(10)
    renderer = Renderer(map)
    action = Action(map)
    
    sim = Simulation(map, renderer, action)