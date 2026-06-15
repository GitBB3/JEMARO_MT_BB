from src.environment import Environment
from src.pathPlanning import PheromoneDescent

class VisionComponent:
    """
    A virtual vision component just here to simulate vision for now.
    """
    def __init__(self, env, damage_map): # Here will probably be the part to change to adapt to a real world
        self.env = env #
        self.damage_map = damage_map # a map of the real damages in the real environment. Format: [modif_coeff for i in range (len(env.grid))] where modif_coeff is a % between 0 and 1 of how different the place is from before the memory map

    def ScreenPlace(self, id_place):
        return self.damage_map[id_place]

class DataManager:
    def MergeData(self, ad_hoc_info): # Dummy component could just generate a slight modification of the current memory. 
        pass

class ComInterface:
    # could determine the area of a placeAgent as the largest surface so that two robots located in two adjacent placeAgents are at communication distance
    def __init__(self, ag_ant):
        self.last_updates = [f"{ag_ant.id}_init"] # list of the ids of the updates received recently by the ant. Every new update received by a same robot or update received by a nex robot should be updating this list.

    def get_news(self): # TODO: Dummy component could just return a boolean (to be defined)
        # If there is another agent close to it
        # If the other agent has some modifications that # WAIT WE NEED A REAL ALGORITHM HERE FOR MANET # Or just dummy for now
        pass

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
    def __init__(self, id_ant, id_place, pheromone, planner_type):
        self.id = id_ant
        self.position = id_place
        self.position_historic = None
        self.pheromone = pheromone
        self.vision = VisionComponent()
        self.memory = Environment()
        self.data_manager = DataManager()
        self.interface = ComInterface()
        self.path_planner = PathPlanner(planner_type)
        # self.navigation = Navigation()

    def deposit(self, amount):
        self.memory.grid[self.position].aggregation(amount)
        # Watch out, it's spreading on its own memory because it's only digital pheromones.

    def PheromoneGenerate(self, image_recognition): # adapt to the input received from the VisionComponent
        new_ph = [1, image_recognition*10] # uncertainty pheromone and entropy pheromone (should diffuse a lot but not evaporate because it should stay), maybe add a damage pheromone which does not move at all
        return new_ph

    def NavigationGoTo(self, destination): # dummy component
        self.position = destination

    def step(self, env, params):
        image_recognition = self.vision.ScreenPlace(env) # dummy component OK
        new_pheromone = self.PheromoneGenerate(image_recognition) # dummy component adapted to the Vision Component OK
        self.deposit(new_pheromone) # OK
        ad_hoc_info = self.interface.get_news() # TODO dummy = just read the memory of the other agants in the communication perimeter
        self.data_manager.MergeData(ad_hoc_info, self.memory) # TODO compute a weighted average of the 2 ?
        id_destination = self.path_planner.PathPlan(self, params) # OK
        self.NavigationGoTo(id_destination) # dummy implementation without real dynamic OK