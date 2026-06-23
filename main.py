import numpy as np
from src.experiment import Experiment

################
## Parameters ##
################

def generate_square_hexagonal_matrix(nb_places):
    """
    Generate an adjacency matrix for a roughly square grid of hexagonal cells.
    Fills from bottom to top, left to right.
    """
    width = int(np.ceil(np.sqrt(nb_places)))
    
    adj_matrix = np.zeros((nb_places, nb_places), dtype=int)
    
    axial_coords = {}
    for current_id in range(nb_places):
        y = current_id // width
        x = current_id % width
        
        r = y
        q = x - (y // 2)
        axial_coords[current_id] = (q, r)

    coords_to_id = {coords: node_id for node_id, coords in axial_coords.items()}
    
    directions = [
        (+1,  0), (0, +1), (-1, +1),
        (-1,  0), (0, -1), (+1, -1)
    ]

    for current_id in range(nb_places):
        q, r = axial_coords[current_id]
        for dq, dr in directions:
            neighbor_coords = (q + dq, r + dr)
            if neighbor_coords in coords_to_id:
                neighbor_id = coords_to_id[neighbor_coords]
                adj_matrix[current_id, neighbor_id] = 1
                
    return adj_matrix

adjacencyMat = generate_square_hexagonal_matrix(100)

agants_lst = np.zeros(len(adjacencyMat))
agants_lst[0] = 5 ## 10 AgAnts on placeAgent 0

lst_semantics = [["RTarget", "GTarget", "GNest", "RThreat"], [1, 1, 0, 0]]
lst_diffusion = [[0.9, 0.1], [0.8, 0.2], 0.3, 0.3]
lst_evaporation = [[0.1, 0.1], [0.1, 0.1], 0.1, 0.1]
lst_types = [0, 3, 2, 1]  # identifier from 0 to 3 if the pheromone is a mark for - respectively - a target, an obstacle, an ag_ant searching for targets or a ghost ag_ant going back to the nest
params = [1.5, 1.0, 0.01, 0.8, 1.0, 1.2, 2.5, 5.5, 0.1, 0.5] # TODO:possibly probable values, to be tuned
ghost_params = params

def unifyFunc(ag_ant, neighbourhood, guidance, params, Dist=0): # TODO: The computation of Dist should be addressed
    unified_pheromone = []
    for neighbour in neighbourhood:
        RTarget = ag_ant.memory.grid[neighbour].pheromoneLevels[guidance[0]]
        GTarget = ag_ant.memory.grid[neighbour].pheromoneLevels[guidance[1]]
        GNest = ag_ant.memory.grid[neighbour].pheromoneLevels[4]
        RThreat = ag_ant.memory.grid[neighbour].pheromoneLevels[5]
        unified_pheromone.append((params[0]*RTarget + params[1]*GTarget + params[2]) / ((params[3]*GNest + params[2])*((Dist + params[4])**(params[5] + params[6]*(RThreat+1))) + params[2]))
    return unified_pheromone

planner_type = "pheromone_descent"
com_type = "gossip"
control_type = "virtual"
vision_type = "virtual"
nest_position = 0

targets = 5
obstacles = 0


################
## Experience ##
################


exp = Experiment(adjacencyMat, agants_lst, lst_semantics, lst_diffusion, lst_evaporation, lst_types, unifyFunc, planner_type, com_type, control_type, vision_type, nest_position)

exp.environment.SpawnTargets(targets)
exp.environment.SpawnObstacles(obstacles)

success, data = exp.Research(params, ghost_params, exp.environment)
if success:
    exp.Analyse(data)
else:
    print("Failure of some kind.")