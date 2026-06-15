import numpy as np

def SelectGuidance(ag_ant, neighbourhood): # neighbourhood could be computed in the function but this way we compute it only once
    """
    Compare the guidance of the pheromone semantics which exist with different dynamics.
    
    :param ag_ant: Object of the AgAnt class, this ag_ant is the one moving.
    :type ag_ant: class AgAnt
    :param neighbourhood: List of index of the placeAgents connected to the placeAgent of the current position.
    :type neighbourhood: list[float]

    :returns: A list of the pheromone dynamics that will offer a better guidance for the Pheromone Descent algorithm.
    :rtype: list[float]
    """
    def Guidance(idx_pheromone, position, neighbourhood, grid_memory):
        fi_s = [grid_memory[i].pheromoneLevels[idx_pheromone] for i in neighbourhood] # total amount of pheromones in the neighbourhood of the current position
        fi_s.append(grid_memory[position].pheromoneLevels[idx_pheromone])
        sum_fi = sum(fi_s)
        if sum_fi==0:
            return 0
        else:
            guidance_value = grid_memory[position].pheromoneLevels[idx_pheromone] / sum_fi - 1/(1+len(neighbourhood))
            for i in neighbourhood:
                fi = grid_memory[i].pheromoneLevels[idx_pheromone] # level of pheromone in neighbour i for pheromone idx_pheromone
                guid_i = fi/sum_fi
                guid_i -= 1/(1+len(neighbourhood))
                if guid_i > guidance_value: guidance_value = guid_i
        return guidance_value

    pheromone_memory = ag_ant.memory
    grid_memory = pheromone_memory.grid
    pheromone = ag_ant.pheromone
    dynamics = pheromone.dynamics
    position = ag_ant.position # Read the position of the ag_ant
    guid_idx = [] # list of pheromone types to take into account
    for i in range (len(dynamics)): # go through the different types of pheromones
        if dynamics[i] and i+1<len(dynamics) and dynamics[i+1]==dynamics[i]: # if the pheromone semantic has 2 dynamics
            guid_short = Guidance(i, position, neighbourhood, grid_memory)
            guid_long = Guidance(i+1, position, neighbourhood, grid_memory)
            if guid_short > guid_long : guid_idx.append(i) # compute the maximum of guidance
            else: guid_idx.append(i+1)
        elif not dynamics[i]: # if the pheromone semantic has a unique dynamic
            guid_idx.append(i)
    return guid_idx # list of the pheromones providing better guidance (indexes in the pheromone list)

def BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params):
    adj_memory = ag_ant.memory.adjacencyMat
    # read the previous position
    pos_past = ag_ant.position_historic
    # find the neighbours of the previous position
    if pos_past is None:
        neighbourhood_past = []
    else:
        neighbourhood_past = [i for i in range (len(adj_memory[pos_past])) if adj_memory[pos_past][i]]
    
    sum_p = sum(unified_pheromone)
    if sum_p == 0 or param_balance == 0:
        balanced_weights = np.zeros(len(unified_pheromone)) # uniform probability if no neighbour is attractive
    else:
        balanced_weights = np.array([param_balance*ph/sum_p for ph in unified_pheromone])
    
    exp_weights = np.exp(balanced_weights - np.max(balanced_weights))
    for i in range (len(neighbourhood)):
        if neighbourhood[i] == pos_past:
            exp_weights[i] *= momentum_params[0]
        elif neighbourhood[i] in neighbourhood_past:
            exp_weights[i] *= momentum_params[1]
    balanced_direction = (exp_weights / np.sum(exp_weights)).tolist()

    return balanced_direction
    

# def PheromoneDescent(ag_ant, params, param_balance=5.5, momentum_params=[0.1,0.5]): #TODO: ag_ant is an important parameter and params should tuned then fixed
def PheromoneDescent(ag_ant, params):
    neighbourhood = [i for i in range (len(ag_ant.memory.adjacencyMat[ag_ant.position])) if ag_ant.memory.adjacencyMat[ag_ant.position][i]]
    guidance = SelectGuidance(ag_ant, neighbourhood)
    unified_pheromone = ag_ant.pheromone.unifyFunc(ag_ant, neighbourhood, guidance, params[:-3]) # TODO: is there a better place to scale the pheromone parameters?
    momentum_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, params[-3], params[-2:]) # param_balance<4 favouring exploration and param_balance>5 favouring exploitation of pheromones
    idx_max = momentum_direction.index(max(momentum_direction)) # TODO: CHANGE CA CE SONT DES PROBAS CE NEST PAS UN MAX!!!
    id_destination = neighbourhood[idx_max]
    return id_destination