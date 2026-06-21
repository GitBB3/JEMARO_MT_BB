from src.environment import Environment
from src.pathPlanning import PheromoneDescent
from src.Comunication import GossipAndMerge

class VisionComponent:
    """
    A virtual vision component just here to simulate vision for now.
    """
    def __init__(self, env, damage_map): # Here will probably be the part to change to adapt to a real world
        self.env = env #
        self.damage_map = damage_map # a map of the real damages in the real environment. Format: [modif_coeff for i in range (len(env.grid))] where modif_coeff is a % between 0 and 1 of how different the place is from before the memory map

    def ScreenPlace(self, id_place):
        # Calcule le neighbourhood
        # return les connaissances dans le neighbourhood
        return self.damage_map[id_place]

class ComInterface: # could determine the area of a placeAgent as the largest surface so that two robots located in two adjacent placeAgents are at communication distance
    def __init__(self, type):
        self.type = type

    def Communicate(self, ag_ant, lst_agants): ## Access to the data of the other robots might be fake
        if self.type == "gossip":
            return GossipAndMerge(ag_ant, lst_agants)

class PathPlanner:
    def __init__(self, type):
        self.type = type
    
    def PathPlan(self, ag_ant, params):
        if self.type == "pheromone_descent":
            return PheromoneDescent(ag_ant, params)

# class Navigation:
#     def goto(self, destination):
#         pass

class AgAnt: # So many "sub-classes" seems scary but let's hope it will help adaptability
    """
    Senses, analyzes, marks, moves accordingly and communicates with the others.
    """
    def __init__(self, id_ant, id_place, pheromone, planner_type, com_type, env):
        self.id = id_ant
        self.position = id_place
        self.position_historic = None
        self.pheromone = pheromone
        self.memory = env
        self.path_planner = PathPlanner(planner_type)
        self.communication_strategy = ComInterface(com_type)

    def deposit(self, amount, time):
        self.memory.grid[self.position].aggregation(amount)
        self.memory.grid[self.position].TimeUpdate(time)

    def AntStep(self, env, lst_agants, params): #lst_agants should not exist to have a real decentralized control (this is equivalent to a comunication device)
        ## Scan the environment & Spread pheromones
        ## Share data with the neighbours
        self.communication_strategy.Communicate(self, lst_agants)

        ## Search for next best position
        id_destination = self.path_planner.PathPlan(self, params)
        
        ## Move to next position
