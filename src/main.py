from simulation.simulation import Simulation
    
if __name__ == "__main__":
    map = Simulation.Map(10)
    renderer = Simulation.Renderer(map)
    action = Simulation.Action(map)
    
    sim = Simulation(map, renderer, action)