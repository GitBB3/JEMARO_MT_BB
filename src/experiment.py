from environment import Environment
from AgAnt import AgAnt
from pheromone import Pheromone

class Experiment:
    def __init__(self, adjacency_matrix, agants_lst, lst_semantics, lst_diffusion, lst_evaporation, unifyFunc, planner_type):
        """
        Define an experiment with limited entry parameters.

        ===Entries: ===
        adjacency_matrix: adjacency matrix of the place Agents.
        agants_lst: list of integers with the number of agents on every placeAgent.
        lst_semantics: list of the semantics names and the associated value 0 if the semantic has only one dynamic and 1 if the semantic has 1 long-range and one short-range semantic.
        lst_diffusion: list of the diffusion rates for every pheromone semantic of lst_semantic list. If the semantic has several dynamics, the several values are in a list.
        lst_evaporation: analog list for the evaporation rate.
        unifyFunc: function to combine the different semantics of pheromones in one unified pheromone.
        planner_type: path planning algorithm chosen for the experiment.
        """
        self.pheromone = Pheromone(lst_semantics, lst_diffusion, lst_evaporation, unifyFunc)
        self.environment = Environment(adjacency_matrix, self.pheromone)
        
        id_ant = 0
        agants_init = []
        for id_place in range (len(agants_lst)):
            if agants_lst[id_place]:
                for i in range (agants_lst[id_place]):
                    agants_init.append(AgAnt(id_ant, id_place, self.pheromone, planner_type))
                    id_ant +=1

        self.agants = agants_init
    
        
