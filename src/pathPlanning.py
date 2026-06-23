import numpy as np
from scipy.sparse.csgraph import dijkstra

def SelectGuidance(ag_ant, neighbourhood): # neighbourhood could be computed in the function but this way we compute it only once
    """
    Compare the guidance of the pheromone semantics which exist with different dynamics.
    
    :param ag_ant: Object of the AgAnt class, this ag_ant is the one moving.
    :type ag_ant: AgAnt
    :param neighbourhood: List of index of the placeAgents connected to the placeAgent of the current position.
    :type neighbourhood: list[float]

    :returns: List of the indexes of the pheromone dynamics that will offer a higher guidance for the Pheromone Descent algorithm.
    :rtype: list[float]
    """
    def Guidance(idx_pheromone, position, neighbourhood, grid_memory):
        """
        Computes the guidance of the pheromone dynamic identified as idx_pheromone.
        :param idx_pheromone: id of the pheromone dynamic studied.
        :type idx_pheromone: int

        :param position: Current position of the AgAnt. Id of the corresponding placeAgent.
        :type position: int

        :param neighbourhood: List of neighbours of the current position. List of placeAgents connected with the placeAgent of the current position.
        :type neighbourhood: list[int]

        :param grid_memory: List of placeAgents with their levels of pheromones according to the memory of the specific AgAnt providing the grid.
        :list grid_memory: list[placeAgent]

        :returns: Numerical value of the guidance of the pheromone idx_pheromone.
        :rtype: float
        """
        fi_s = [grid_memory[i].pheromoneLevels[idx_pheromone] for i in neighbourhood] # total amount of pheromones in the neighbourhood of the current position
        fi_s.append(grid_memory[position].pheromoneLevels[idx_pheromone])
        sum_fi = sum(fi_s)
        if sum_fi < 1e-6: # to avoid inequalities with a strict equality condition "=="
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
    """
    Associates with every placeAgent of the neighbourhood a probability to go considering the value of the unified pheromone in its place, a given parameter param_balance to favour a stochastic or deterministic exploration and a parameter momentum_param to avoid U-turns.
    
    :param unified_pheromone: List of numerical values of the unified pheromone in every placeAgent of the neighbourhood.
    :type unified_pheromone: list[float]

    :param ag_ant: Object of the AgAnt class, this ag_ant is the one moving.
    :type ag_ant: AgAnt

    :param neighbourhood: List of neighbours of the current position. List of placeAgents connected with the placeAgent of the current position.
    :type neighbourhood: list[int]

    :param param_balance: Parameter favouring stochastic exploration or deterministic exploitation of pheromones to cover the environment. param_balance<4 favouring exploration and param_balance>5 favouring exploitation of pheromones.
    :type param_balance: float

    :param momentum_params: Weights influencing the probababilities to go towards a placeAgent of the neighbourhood to avoid U-Turns and going back to recently visited areas.
    :type momentum_params: list[float]

    :returns: List of the probabilities associated to every placeAgent of the neighbourhood with regard to how probable it is to move to this position at next move.
    :rtype: list[float]
    """
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
    if len(neighbourhood) == 1:
        return [1]        
    elif momentum_params[0] !=0 or momentum_params[1] != 0:
        for i in range (len(neighbourhood)):
            if neighbourhood[i] == pos_past:
                exp_weights[i] *= momentum_params[0]
            elif neighbourhood[i] in neighbourhood_past:
                exp_weights[i] *= momentum_params[1]
    balanced_direction = (exp_weights / np.sum(exp_weights)).tolist()

    return balanced_direction
    

# def PheromoneDescent(ag_ant, params, param_balance=5.5, momentum_params=[0.1,0.5]): #TODO: ag_ant is an important parameter and params should tuned then fixed. is there a better place to scale the pheromone parameters?
def PheromoneDescent(ag_ant, params, Dist=0):
    """
    Computes the index of the placeAgent where a given AgAnt should move at next step.

    :param ag_ant: Object of the AgAnt class, this ag_ant is the one moving.
    :type ag_ant: AgAnt

    :param params: List of parameters to tune this PathPlanning algorithm: The one before before last influences whether the AgAnt moves more stochastically or more deterministically, the 2 last ones influence the tendency of the AgAnt to do U-turns and the first others are required to unify all semantics of pheromones in one unified one.
    :type params: list[float]

    :returns: Index of the placeAgent where the AgAnt should go next.
    """
    neighbourhood = [i for i in range (len(ag_ant.memory.adjacencyMat[ag_ant.position])) if ag_ant.memory.adjacencyMat[ag_ant.position][i]] # subset of the ensemble of placeAgent positions.
    if not len(neighbourhood):
        return ag_ant.position
    else:
        guidance = SelectGuidance(ag_ant, neighbourhood) # subset of the ensemble of pheromone dynamics.
        unified_pheromone = ag_ant.pheromone.unifyFunc(ag_ant, neighbourhood, guidance, params[:-3], Dist) # returns a list of the values of the unified pheromone in every placeAgent of the neighbourhood, computed with the pheromones dynamics giving better guidance.
        momentum_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, params[-3], params[-2:]) # list of probabilities to go to each placeAgent of the neighbourhood.
        id_destination = int(np.random.choice(neighbourhood, p=momentum_direction)) # choice of the next position weighted by the previous probabilities.
        return id_destination

def Ghost_PheromoneDescent(ghost, ghost_params):
    """
    Computes.
    """
    neighbourhood = [i for i in range (len(ghost.memory.adjacencyMat[ghost.position])) if ghost.memory.adjacencyMat[ghost.position][i]] # subset of the ensemble of placeAgent positions.
    if not len(neighbourhood):
        return ghost.position
    else:
        guidance = SelectGuidance(ghost, neighbourhood) # subset of the ensemble of pheromone dynamics.
        Dist = int(dijkstra(np.array(ghost.memory.adjacencyMat), directed=False, indices=ghost.position)[ghost.nest_position])
        unified_pheromone = ghost.pheromone.unifyFunc(ghost, neighbourhood, guidance, ghost_params[:-3], Dist) # returns a list of the values of the unified pheromone in every placeAgent of the neighbourhood, computed with the pheromones dynamics giving better guidance.
        momentum_direction = BalanceDirectionWithMomentum(unified_pheromone, ghost, neighbourhood, ghost_params[-3], ghost_params[-2:]) # list of probabilities to go to each placeAgent of the neighbourhood.
        id_destination = int(np.random.choice(neighbourhood, p=momentum_direction)) # choice of the next position weighted by the previous probabilities.
        return id_destination
