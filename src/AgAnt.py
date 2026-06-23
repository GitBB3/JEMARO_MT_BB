from src.environment import Environment
from src.pathPlanning import PheromoneDescent, Ghost_PheromoneDescent
from src.Comunication import GossipAndMerge

class VisionComponent:
    def __init__(self, type):
        self.type = type
    
    def Scan(self, ag_ant, real_env):
        if self.type == "virtual":
            return real_env.grid[ag_ant.position].type

class Control:
    def __init__(self, type):
        self.type = type
    
    def GoTo(self, ag_ant, position):
        if self.type == "virtual":
            ag_ant.position = position

class ComInterface: # could determine the area of a placeAgent as the largest surface so that two robots located in two adjacent placeAgents are at communication distance
    def __init__(self, type):
        self.type = type

    def Communicate(self, ag_ant, lst_agants): ## Access to the data of the other robots might be fake
        if self.type == "gossip":
            GossipAndMerge(ag_ant, lst_agants)

class PathPlanner:
    def __init__(self, type):
        self.type = type
    
    def PathPlan(self, ag_ant, params):
        if self.type == "pheromone_descent":
            return PheromoneDescent(ag_ant, params)
        
        elif self.type == "ghost_pheromone":
            return Ghost_PheromoneDescent(ag_ant, params)


class AgAnt: # So many "sub-classes" seems scary but let's hope it will help adaptability
    """
    Senses, analyzes, marks, moves accordingly and communicates with the others.
    """
    def __init__(self, id_ant, id_place, pheromone, planner_type, com_type, control_type, vision_type, env):
        self.id = id_ant
        self.position = id_place
        self.position_historic = None
        self.pheromone = pheromone
        self.memory = env
        self.nest_position = env.nest_position
        self.path_planner = PathPlanner(planner_type)
        self.communication_strategy = ComInterface(com_type)
        self.controller = Control(control_type)
        self.vision = VisionComponent(vision_type)
        self.ghosts = []
    
    def Init_Ghosts(self, nb_ghosts=20):
        for i in range (nb_ghosts):
            self.ghosts.append(GhostAnt(i, self.position, self.pheromone, "ghost_pheromone", "virtual", "virtual", self.memory))

    def GhostBackPropagation(self, ghost_params, ghost_speed=3):
        for _ in range (ghost_speed):
            for i in range (len(self.ghosts)-1, -1, -1): # to avoid index change when poping elements
                ghost = self.ghosts[i]
                finished = ghost.GhostStep(ghost_params)
                if finished:
                    self.ghosts.pop(i)

    def MarkAs(self, type, amount):
        nb_ph = len(self.pheromone.semantics)
        for i in range (nb_ph):
            if self.pheromone.types[i] == type:
                add = [0]*nb_ph
                add[i] = amount[i]
                self.memory.grid[self.position].aggregation(add)

    def DepositPheromone(self, scanned_type, time, ghost_params, amount=None): #tune amount if needed
        if amount==None: amount=[10]*len(self.pheromone.semantics)
        self.MarkAs(2, amount)
        if scanned_type == self.memory.grid[self.position].type:
            if scanned_type == "obstacle":
                self.MarkAs(1, amount)
            elif scanned_type == "target":
                self.MarkAs(0, amount)
        elif scanned_type == "target":
            self.memory.grid[self.position].type = "target"
            self.MarkAs(0, amount)
            self.memory.grid[self.position].TimeUpdate(time)
            self.Init_Ghosts()
        elif scanned_type == "obstacle":
            self.memory.grid[self.position].type = "obstacle"
            self.MarkAs(1, amount)
            self.memory.grid[self.position].TimeUpdate(time)
        self.GhostBackPropagation(ghost_params)

class GhostAnt:
    """
    Ghost AgAnt.
    """
    def __init__(self, id_ant, id_place, pheromone, planner_type, control_type, vision_type, env):
        self.id = id_ant
        self.position = id_place
        self.position_historic = None
        self.pheromone = pheromone
        self.memory = env
        self.nest_position = env.nest_position
        self.path_planner = PathPlanner(planner_type)
        self.controller = Control(control_type)
        self.vision = VisionComponent(vision_type)
    
    def MarkAs(self, type, amount):
        nb_ph = len(self.pheromone.semantics)
        for i in range (nb_ph):
            if self.pheromone.types[i] == type:
                add = [0]*nb_ph
                add[i] = amount[i]
                self.memory.grid[self.position].aggregation(add)

    def Ghost_DepositPheromone(self, scanned_type, amount=None): #tune amount if needed
        if amount==None: amount=[10]*len(self.pheromone.semantics)
        self.MarkAs(3, amount)
        if self.position == self.nest_position:
            return True
        elif scanned_type == "obstacle":
            self.MarkAs(1, amount)
            return False
        elif scanned_type == "target":
            self.MarkAs(0, amount)
            return False
    
    def GhostStep(self, params): #lst_agants should not exist to have a real decentralized control (this is equivalent to a comunication device)
        ## Search for next best position
        id_destination = self.path_planner.PathPlan(self, params) # Pheromone descent
        
        ## Move to next position
        self.position_historic = self.position
        self.controller.GoTo(self, id_destination) # Dummy version
        
        ## Scan the environment & Spread pheromones
        scanned_type = self.vision.Scan(self, self.memory)
        finished = self.Ghost_DepositPheromone(scanned_type)
        
        return finished