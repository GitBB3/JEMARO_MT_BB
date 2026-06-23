class Pheromone:
    """
    Store all the paramereters of pheromone in a class. Will enable to modify the parameters in the simulation.

    ===Entries: ===
    lst_semantics: list of the semantics names and the associated value 0 if the semantic has only one dynamic and 1 if the semantic has 1 long-range and one short-range semantic.
    lst_diffusion: list of the diffusion rates for every pheromone semantic of lst_semantic list. If the semantic has several dynamics, the several values are in a list.
    lst_evaporation: analog list for the evaporation rate.
    """
    def __init__(self, lst_semantics, lst_diffusion, lst_evaporation, lst_types, unifyFunc):
        semantics = []
        diffusion = []
        evaporation = []
        dynamics = [] # identifier for every pair of dynamic pheromone with the same semantic
        types = [] # identifier from 0 to 3 if the pheromone is a mark for - respectively - a target, an obstacle, an ag_ant searching for targets or a ghost ag_ant going back to the nest
        for i in range (len(lst_semantics[0])):
            if lst_semantics[1][i]:
                semantics.append(lst_semantics[0][i] + "_short") # check si ça marche
                semantics.append(lst_semantics[0][i] + "_long")
                diffusion.append(lst_diffusion[i][0])
                diffusion.append(lst_diffusion[i][1])
                evaporation.append(lst_evaporation[i][0])
                evaporation.append(lst_evaporation[i][1])
                dynamics.append(i+1) # i+1 to avoid 0 which means unique dynamic
                dynamics.append(i+1)
                types.append(lst_types[i])
                types.append(lst_types[i])
            else:
                semantics.append(lst_semantics[0][i])
                diffusion.append(lst_diffusion[i])
                evaporation.append(lst_evaporation[i])
                dynamics.append(0)
                types.append(lst_types[i])
        self.semantics = semantics
        self.diffusion = diffusion
        self.evaporation = evaporation
        self.dynamics = dynamics
        self.unifyFunc = unifyFunc
        self.types = types


# lst_semantics = [["RTarget", "GTarget", "GNest", "RThreat"], [1, 1, 0, 0]]
# lst_diffusion = [[0.9, 0.1], [0.8, 0.2], 0.3, 0.3]
# lst_evaporation = [[0.1, 0.1], [0.1, 0.1], 0.1, 0.1]
# pheromone_example = Pheromone(lst_semantics, lst_diffusion, lst_evaporation)
# print(pheromone_example.semantics, pheromone_example.diffusion, pheromone_example.evaporation, pheromone_example.dynamics)