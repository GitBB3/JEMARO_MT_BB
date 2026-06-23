def Merge(ant_ref, ant_near):
    nb_places = len(ant_ref.memory.grid)
    for place in range (nb_places):
        if ant_ref.memory.grid[place].timestamp < ant_near.memory.grid[place].timestamp:
            ant_ref.memory.grid[place].pheromoneLevels = list(ant_near.memory.grid[place].pheromoneLevels)
            ant_ref.memory.grid[place].timestamp = ant_near.memory.grid[place].timestamp
            if ant_ref.memory.grid[place].type != ant_near.memory.grid[place].type:
                ant_ref.memory.grid[place].type = ant_near.memory.grid[place].type

def GossipAndMerge(ag_ant, lst_agants):
    # Get the neighbourhood
    neighbourhood = [i for i in range (len(ag_ant.memory.adjacencyMat[ag_ant.position])) if ag_ant.memory.adjacencyMat[ag_ant.position][i]]
    neighbourhood.append(ag_ant.position)
    # Check if the neighbourhood is crowded ## 2 first lines should be changed by "detection of other robots"
    for ant in lst_agants:
        # Merge with the neighbours based on latest timestamp
        if ant.id !=ag_ant.id and ant.position in neighbourhood:
            Merge(ag_ant, ant)