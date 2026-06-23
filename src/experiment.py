import copy

from src.environment import Environment
from src.AgAnt import AgAnt
from src.pheromone import Pheromone

class Experiment:
    def __init__(self, adjacency_matrix, agants_lst, lst_semantics, lst_diffusion, lst_evaporation, lst_types, unifyFunc, planner_type, com_type, control_type, vision_type, nest_position):
        """
        Define an experiment with limited entry parameters.

        ===Entries: ===
        :param adjacency_matrix: adjacency matrix of the place Agents.
        :type adjacency_matrix: lst[lst[1 or 0]]
        :param agants_lst: list of integers with the number of agents on every placeAgent.
        :type agants_lst: lst[int]
        :param lst_semantics: list of the semantics names and the associated value 0 if the semantic has only one dynamic and 1 if the semantic has 1 long-range and one short-range semantic.
        :type lst_semantics: [lst[str], lst[1 or 0]]
        :param lst_diffusion: list of the diffusion rates for every pheromone semantic of lst_semantic list. If the semantic has several dynamics, the several values are in a list.
        :type lst_diffusion: lst[lst[float] or float]
        :param lst_evaporation: analog list for the evaporation rate.
        :type lst_evaporation: lst[lst[float] or float]
        :param unifyFunc: function to combine the different semantics of pheromones in one unified pheromone.
        :type unifyFunc: func
        :param planner_type: path planning algorithm chosen for the experiment.
        :type planner_type: str
        """
        self.time = 0
        self.pheromone = Pheromone(lst_semantics, lst_diffusion, lst_evaporation, lst_types, unifyFunc)
        self.environment = Environment(adjacency_matrix, self.pheromone, nest_position)
        
        id_ant = 0
        agants_init = []
        for id_place in range (len(agants_lst)):
            if agants_lst[id_place]:
                for i in range (int(agants_lst[id_place])):
                    agants_init.append(AgAnt(id_ant, id_place, self.pheromone, planner_type, com_type, control_type, vision_type, copy.deepcopy(self.environment)))
                    id_ant +=1

        self.agants = agants_init
    
    def StepResearch(self, params, ghost_params, real_env):
        # once, run the exploration with browninan movement ants to compute a threshold of runtime error if the simulation is taking too long
        
        nb_ants = len(self.agants)

        ## Scan the environment & Spread pheromones
        for i in range (nb_ants):
            ant = self.agants[i]
            scanned_type = ant.vision.Scan(ant, real_env) ## read type of the placeAgent in the real_env
            ant.DepositPheromone(scanned_type, self.time, ghost_params)
        
        ## Share data with the neighbours
        for i in range (nb_ants):
            ant = self.agants[i]
            ant.communication_strategy.Communicate(ant, self.agants) # Timestamp based version
        
        ## Search for next best position and Move
        for i in range (nb_ants):
            ant = self.agants[i]
            id_destination = ant.path_planner.PathPlan(ant, params) # Pheromone descent
            ant.position_historic = ant.position
            ant.controller.GoTo(ant, id_destination) # Dummy version
            ant.memory.diffusion()
            ant.memory.env_evaporation()

        # stop the search when all the targets have been found or all the env has been covered
        # pass # return success, data
    
    def Research(self, params, ghost_params, real_env, max_steps=10000):
        """
        research.
        """
        if not self.agants:
            return None, None
        
        # 1. Identifier et compter les cibles réelles uniques dans le monde réel
        real_target_positions = [id_place for id_place, place in enumerate(real_env.grid) if place.type == "target"]
        total_targets_count = len(real_target_positions)

        print(f"🚀 Début de l'expérience. Objectif : {total_targets_count} cibles à découvrir par {len(self.agants)} agents.")

        # Initialisation des compteurs de temps demandés
        time_all_targets_discovered_globally = None
        time_all_agents_know_all_targets = None
        remaining_targets = set(real_target_positions)

        # 2. Boucle principale de simulation
        while self.time < max_steps and time_all_agents_know_all_targets == None:
            self.StepResearch(params, ghost_params, real_env)
            
            # --- CONDITION 1 : Toutes les cibles découvertes par au moins un agent ---
            if time_all_targets_discovered_globally is None:
                # On crée un ensemble des cibles qu'il reste à découvrir
                # (à initialiser de préférence juste avant la boucle while : remaining_targets = set(real_target_positions))
                
                for ant in self.agants:
                    # On retire de l'ensemble les cibles que cette fourmi a validées dans sa mémoire
                    # .discard() retire l'élément s'il existe, et ne fait rien (sans erreur) s'il n'y est pas
                    for target_pos in list(remaining_targets): 
                        if ant.memory.grid[target_pos].type == "target":
                            remaining_targets.discard(target_pos)
                
                # Si l'ensemble est vide, c'est que toutes les cibles ont été touchées au moins une fois
                if not remaining_targets:
                    time_all_targets_discovered_globally = self.time

            # --- CONDITION 2 : Consensus total (intersection / chaque agent sait tout) ---
            all_agents_completed = True
            for ant in self.agants:
                ant_found_count = sum(1 for place in ant.memory.grid if place.type == "target")
                
                if ant_found_count < total_targets_count:
                    all_agents_completed = False
                    break # Inutile de vérifier les autres agents pour ce tour
            
            if all_agents_completed:
                time_all_agents_know_all_targets = self.time

            self.time += 1

        # 3. Bilans et retours des résultats
        if time_all_agents_know_all_targets is None:
            return time_all_targets_discovered_globally, None

        success = time_all_agents_know_all_targets
        data = [time_all_targets_discovered_globally, time_all_agents_know_all_targets]

        return success, data
    
    def Analyse(self, data):
        print(f"[Temps: {data[0]}] Toutes les cibles ont été découvertes par au moins un agent !")
        print(f"[Temps: {data[1]}] Condition d'arrêt atteinte : TOUS les agents ont découvert TOUTES les cibles !")