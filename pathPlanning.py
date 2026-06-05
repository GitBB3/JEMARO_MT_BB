def SelectGuidance(ag_ant):
    """
    Compare the guidance of the pheromone semantics which exist with different dynamics.
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
    adj_memory = pheromone_memory.adjacencyMat
    grid_memory = pheromone_memory.grid
    pheromone = ag_ant.pheromone
    dynamics = pheromone.dynamics
    position = ag_ant.position # Read the position of the ag_ant
    neighbourhood = [i for i in range (len(adj_memory[position])) if adj_memory[position][i]] # find the neighbours of the current position placeAgent
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

def BalanceDirection(single_pheromone):
    pass

def MomentumAddition(balanced_direction):
    pass

def PheromoneDescent(ag_ant, params): #TODO: ag_ant is an important parameter and params should tuned then fixed
    guidance = SelectGuidance(ag_ant)
    unified_pheromone = ag_ant.pheromone.unifyFunc(ag_ant, guidance, params) # TODO: is there a better place to scale the pheromone parameters?
    balanced_direction = BalanceDirection(unified_pheromone)
    momentum_direction = MomentumAddition(balanced_direction)
    return momentum_direction
