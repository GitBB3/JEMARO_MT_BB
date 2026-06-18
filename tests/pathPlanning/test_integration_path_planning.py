import pytest
import numpy as np

from src.pathPlanning import PheromoneDescent

###########
## Mocks ##
###########

class MockPlaceAgent:
    def __init__(self, pheromoneLevels):
        self.pheromoneLevels = pheromoneLevels

class MockEnvironment:
    def __init__(self, grid, adjacencyMat):
        self.grid = grid
        self.adjacencyMat = adjacencyMat

class MockPheromone:
    def __init__(self, dynamics, unify_func):
        self.dynamics = dynamics
        self.unifyFunc = unify_func

class MockAnt:
    def __init__(self, position, position_historic, grid, dynamics, unify_func, adjacencyMat):
        self.memory = MockEnvironment(grid, adjacencyMat)
        self.pheromone = MockPheromone(dynamics, unify_func)
        self.position = position
        self.position_historic = position_historic

###############
## Variables ##
###############

## Pheromones definition ###################################################################################################################
lst_semantics = [["Ph"], [0]]
lst_diffusion = [0]
lst_evaporation = [0]
def unifyFunc(ag_ant, neighbourhood, guidance, params, Dist=0):
        unified_pheromone = []
        for neighbour in neighbourhood:
            unified_pheromone.append(ag_ant.memory.grid[neighbour].pheromoneLevels[0])
        return unified_pheromone

# pheromone_example = Pheromone(lst_semantics, lst_diffusion, lst_evaporation, unifyFunc)


## Unambiguous line ########################################################################################################################
adjacencyMat_line = np.array([
        #0  1  2  3  4  5  6  7
        [0, 1, 0, 0, 0, 1, 0, 0],  # 0 connected to 1 (good) and 5 (dead-end)
        [1, 0, 0, 0, 1, 0, 0, 0],  # 1 connected to 0 and 4 (good)
        [0, 0, 0, 1, 0, 0, 0, 1],  # 2 (Cible) connected to 3 (good) and 7 (dead-end)
        [0, 0, 1, 0, 1, 0, 0, 0],  # 3 connected to 4 (good) and 2 (good)
        [0, 1, 0, 1, 0, 0, 1, 0],  # 4 connected to 1, 3 (good) and 6 (dead-end)
        [1, 0, 0, 0, 0, 0, 0, 0],  # 5 dead-end
        [0, 0, 0, 0, 1, 0, 0, 0],  # 6 dead-end
        [0, 0, 1, 0, 0, 0, 0, 0],  # 7 dead-end
    ])
grid_line = [
        MockPlaceAgent([1.0]),   # Node 0 (Start)
        MockPlaceAgent([2.0]),   # Node 1
        MockPlaceAgent([100.0]), # Node 2 (Target - Global maximum)
        MockPlaceAgent([50.0]),  # Node 3
        MockPlaceAgent([10.0]),  # Node 4
        MockPlaceAgent([0.0]),   # Node 5 (dead-end)
        MockPlaceAgent([0.0]),   # Node 6 (dead-end)
        MockPlaceAgent([0.0]),   # Node 7 (dead-end)
    ]
expected_steps_line = [0, 1, 4, 3, 2]
env_line = MockEnvironment(grid_line, adjacencyMat_line)

###########
## Tests ##
###########


@pytest.mark.parametrize(["environment", "expected_steps"], [
    (env_line, expected_steps_line), # unambiguous line
])

def test_INTEGRATION_PATH_PLANNING_pheromone_descent_1_pheromone_flavour_global_min_search(environment, expected_steps):
    """
    Check that an ant can find a maximum of pheromone in a static gradient map.
    """
    steps_history = [0]
    steps = 0
    position = 0
    position_historic = None
    ag_ant = MockAnt(position, position_historic, environment.grid, [0], unifyFunc, environment.adjacencyMat)
    params = [1000, 0.5, 0.3] # balance_parameter of 1000 to favour exploitation, U-turns penalized by 50% and possible U-turns reduces by 30%
    security_threshold = 1000
    while ag_ant.position != expected_steps[-1] and steps < security_threshold:
        next_position = PheromoneDescent(ag_ant, params)
        steps_history.append(next_position)

        ag_ant.position_historic = ag_ant.position
        ag_ant.position = next_position

        steps += 1
    assert steps_history == expected_steps

    # Loop: study how long it takes to find the maximum of pheromone with different parameters and pheromone maps. check 
    # Use a set of pytest environments
    # create a function that runs the gradient descent until the global minimum is found.
        # runs the search several times per environment to check even with the random choices
        # assert we find the minimum
        # assert the time is lower than with a random search (maybe implement it by setting the balance_parameter to 0)

@pytest.mark.parametrize(["environment", "expected_steps"], [
    (env_line, expected_steps_line), # unambiguous line
])
def test_INTEGRATION_PATH_PLANNING_pheromone_descent_1_pheromone_flavour_global_min_search_comparison_exploration_exploitation(environment, expected_steps):
    """
    Check that exploitation of pheromones improves the efficiency of the search compared to a stochastic exploration of the environment.
    """

    nb_exp = 100
    nb_success_exploration = 0
    nb_success_exploitation = 0
    security_threshold = 1000

    params = [5.5, 0.5, 0.3] # balance_parameter > 4 to favour exploitation, U-turns penalized by 50% and possible U-turns reduces by 30%
    for _ in range (nb_exp):
        steps_history = [0]
        steps = 0
        position = 0
        position_historic = None
        ag_ant = MockAnt(position, position_historic, environment.grid, [0], unifyFunc, environment.adjacencyMat)
        while ag_ant.position != expected_steps[-1] and steps < security_threshold:
            next_position = PheromoneDescent(ag_ant, params)
            steps_history.append(next_position)

            ag_ant.position_historic = ag_ant.position
            ag_ant.position = next_position

            steps += 1
        if steps_history == expected_steps:
            nb_success_exploitation += 1
    
    params = [3.5, 0.5, 0.3] # balance_parameter < 4 to favour exploration, U-turns penalized by 50% and possible U-turns reduces by 30%
    for _ in range (nb_exp):
        steps_history = [0]
        steps = 0
        position = 0
        position_historic = None
        ag_ant = MockAnt(position, position_historic, environment.grid, [0], unifyFunc, environment.adjacencyMat)
        while ag_ant.position != expected_steps[-1] and steps < security_threshold:
            next_position = PheromoneDescent(ag_ant, params)
            steps_history.append(next_position)

            ag_ant.position_historic = ag_ant.position
            ag_ant.position = next_position

            steps += 1
        if steps_history == expected_steps:
            nb_success_exploration += 1

    assert nb_success_exploration <= nb_success_exploitation


def test_INTEGRATION_PATH_PLANNING_pheromone_descent_1_pheromone_flavour_exiting_dead_end():
    """
    Check that, while avoiding U-turns, the AgAnt will go backwards if it leads to its only neighbour available.
    """
    #TODO: I see a risk of pheromone trap here, going back and forth for ever if the U-turn parameter is not strong enough.

    position = 5
    position_historic = 0
    ag_ant = MockAnt(position, position_historic, env_line.grid, [0], unifyFunc, env_line.adjacencyMat)
    params = [5.5, 0, 0]
    next_position = PheromoneDescent(ag_ant, params)
    assert next_position == 0

def test_INTEGRATION_PATH_PLANNING_pheromone_descent_1_pheromone_flavour_no_neighbours():
    """
    Check that the algorithm is robust to the absence of positions neighbouring the current position.
    """
    isolated_adjacency = np.zeros((4,4))
    ag_ant = MockAnt(0, None, env_line.grid, [0], unifyFunc, isolated_adjacency)
    params = [5.5, 0, 0]
    
    assert PheromoneDescent(ag_ant, params) == 0