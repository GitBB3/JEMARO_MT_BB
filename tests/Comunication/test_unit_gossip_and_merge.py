import pytest
import numpy as np

from src.placeAgent import placeAgent
from src.Comunication import GossipAndMerge

###########
## Mocks ##
###########

class MockEnvironment:
    def __init__(self, grid, adjacencyMat):
        self.grid = grid
        self.adjacencyMat = adjacencyMat

class MockAnt:
    def __init__(self, id, position, grid, adjacencyMat):
        self.id = id
        self.position = position
        self.memory = MockEnvironment(grid, adjacencyMat)

class MockPheromone:
    def __init__(self, semantics, evaporation):
        self.semantics = semantics
        self.evaporation = evaporation

###########
## Tests ##
###########

## Test avec 3 placeAgents, un au milieu et on vérifie que sa valeur après application de la fonction est celle du maximum entre ses 2 voisins

def test_UNIT_comunication_newest_data_chosen():
    """
    Check that for several ag_ants on the same placeAgent, the one to which we apply the GossipAndMerge will take the pheromone value of the ag_ants that updated it the latest.
    """
    # A line of 3 placeAgents with id=1 in the middle
    adj_mat = np.array([[0]])  
    ph = MockPheromone(["Unique"], [0.1])

    # Data AgAnt 0
    grid0 = [placeAgent(0, ph, "basic")]
    grid0[0].pheromoneLevels = [0]
    grid0[0].timestamp = 0
    ag_ant0 = MockAnt(0, 0, grid0, adj_mat)

    # Data AgAnt 1
    grid1 = [placeAgent(0, ph, "basic")]
    grid1[0].pheromoneLevels = [10]
    grid1[0].timestamp = 10
    ag_ant1 = MockAnt(1, 0, grid1, adj_mat)

    # Data AgAnt 2
    grid2 = [placeAgent(0, ph, "basic")]
    grid2[0].pheromoneLevels = [100]
    grid2[0].timestamp = 100
    grid2[0].type = "obstacle"
    ag_ant2 = MockAnt(2, 0, grid2, adj_mat)

    lst_agants = [ag_ant0, ag_ant1, ag_ant2]
        
    GossipAndMerge(ag_ant1, lst_agants)

    assert grid0[0].pheromoneLevels[0] == 0 and grid0[0].timestamp == 0 and grid0[0].type == "basic"
    assert grid1[0].pheromoneLevels[0] == 100 and grid1[0].timestamp == 100 and grid1[0].type == "obstacle"
    assert grid2[0].pheromoneLevels[0] == 100 and grid2[0].timestamp == 100 and grid2[0].type == "obstacle"

def test_UNIT_comunication_max_distance_comunication():
    """
    Check that, for several ag_ants in the neighbourhood of the one to which we apply the GossipAndMerge, the latter will take the pheromone value of the ag_ants that updated it the latest.
    """
    # A line of 3 placeAgents with id=1 in the middle
    adj_mat = np.array([[0, 1], [1, 0]])  
    ph = MockPheromone(["Unique"], [0.1])

    # Data AgAnt 0
    grid0 = [placeAgent(0, ph, "basic"), placeAgent(1, ph, "basic")]
    grid0[0].pheromoneLevels = [0]
    grid0[0].timestamp = 0
    ag_ant0 = MockAnt(0, 0, grid0, adj_mat)

    # Data AgAnt 1
    grid1 = [placeAgent(0, ph, "basic"), placeAgent(1, ph, "basic")]
    grid1[0].pheromoneLevels = [10]
    grid1[0].timestamp = 10
    ag_ant1 = MockAnt(1, 1, grid1, adj_mat)

    # Data AgAnt 2
    grid2 = [placeAgent(0, ph, "basic"), placeAgent(1, ph, "basic")]
    grid2[0].pheromoneLevels = [100]
    grid2[0].timestamp = 100
    grid2[0].type = "obstacle"
    ag_ant2 = MockAnt(2, 1, grid2, adj_mat)

    lst_agants = [ag_ant0, ag_ant1, ag_ant2]
        
    GossipAndMerge(ag_ant0, lst_agants)

    assert grid0[0].pheromoneLevels[0] == 100 and grid0[0].timestamp == 100 and grid0[0].type == "obstacle"
    assert grid1[0].pheromoneLevels[0] == 10 and grid1[0].timestamp == 10 and grid1[0].type == "basic"
    assert grid2[0].pheromoneLevels[0] == 100 and grid2[0].timestamp == 100 and grid2[0].type == "obstacle"

def test_UNIT_comunication_distance_threshold():
    """
    Check that, two robots cannot communicate if they are not direct neighbours.
    """
    # A line of 3 placeAgents with id=1 in the middle
    adj_mat = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]) 
    ph = MockPheromone(["Unique"], [0.1])

    # Data AgAnt 0
    grid0 = [placeAgent(0, ph, "basic"), placeAgent(1, ph, "basic"), placeAgent(2, ph, "basic")]
    grid0[0].pheromoneLevels = [0]
    grid0[0].timestamp = 0
    ag_ant0 = MockAnt(0, 0, grid0, adj_mat)

    # Data AgAnt 2
    grid2 = [placeAgent(0, ph, "basic"), placeAgent(1, ph, "basic"), placeAgent(2, ph, "basic")]
    grid2[0].pheromoneLevels = [100]
    grid2[0].timestamp = 100
    grid2[0].type = "obstacle"
    ag_ant2 = MockAnt(2, 2, grid2, adj_mat)

    lst_agants = [ag_ant0, ag_ant2]
        
    GossipAndMerge(ag_ant0, lst_agants)

    assert grid0[0].pheromoneLevels[0] == 0 and grid0[0].timestamp == 0 and grid0[0].type == "basic"
    assert grid2[0].pheromoneLevels[0] == 100 and grid2[0].timestamp == 100 and grid2[0].type == "obstacle"