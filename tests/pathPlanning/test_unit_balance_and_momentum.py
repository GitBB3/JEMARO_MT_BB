import pytest
import numpy as np
from src.pathPlanning import BalanceDirectionWithMomentum

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

class MockAnt:
    def __init__(self, position, position_historic, grid, adjacencyMat):
        self.memory = MockEnvironment(grid, adjacencyMat)
        self.position = position
        self.position_historic = position_historic


###########
## Tests ##
###########

@pytest.mark.parametrize("momentum_params", [
    ([1, 1]), # no penalty on the U-turns
    ([0.5, 0.7]), # penalty on U-turns and places potentially already visited
    ([0.5, 1]), # penalty only on U-turns
])
def test_UNIT_balance_and_momentum_initial_step(momentum_params):
    """
    Check that the initial step is fully stochastic.
    The position and position_historic are the same and the probabilities to go in any neighbour should be equal.
    """
    position = 0
    position_historic = None
    pheromoneLevels = 0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels),  MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    adjacencyMat = [[0, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [0, 0, 0, 0, 0]
    param_balance = 5.5
    
    neighbourhood = [1, 2, 3, 4, 5]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)
    result = np.max(np.array(balanced_direction)) - np.array(balanced_direction)
    assert result == pytest.approx([0,0,0,0,0])
    assert sum(balanced_direction) == pytest.approx(1)

def test_UNIT_balance_and_momentum_u_turn_avoidance():
    """
    Check that the probability to do a U-turn is weighted by momentum_params[0].
    
    :param momentum_params: List of 2 percentages representing the weight that will balance the probability to go back to the previous placeAgent or in the direction of the placeAgent before last.
    :type momentum_params: list[float]

    """
    position = 1
    position_historic = 0
    pheromoneLevels = 1.0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    adjacencyMat = [[0, 1, 0, 0],
                    [1, 0, 1, 1],
                    [0, 1, 0, 0],
                    [0, 1, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [1, 1, 1]
    param_balance = 5.5
    
    neighbourhood = [0, 2, 3]

    momentum_params = [0.5, 1]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)

    assert balanced_direction == [0.2, 0.4, 0.4]
    assert sum(balanced_direction) == pytest.approx(1)

def test_UNIT_balance_and_momentum_large_u_turn_avoidance():
    """
    Check that the probability to go in a direction already explored is weighted by momentum_params[1].
    
    :param momentum_params: List of 2 percentages representing the weight that will balance the probability to go back to the previous placeAgent or in the direction of the placeAgent before last.
    :type momentum_params: list[float]

    """
    position = 2
    position_historic = 1
    pheromoneLevels = 1.0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    adjacencyMat = [[0, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [1, 1, 1]
    param_balance = 5.5
    
    neighbourhood = [1, 3, 4]
    momentum_params = [0, 0.5]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)
    assert balanced_direction == pytest.approx([0, 1/3, 2/3])
    assert sum(balanced_direction) == pytest.approx(1)

@pytest.mark.parametrize("momentum_params", [
    ([1, 1]), # no penality on the U-turns
    ([0.5, 0.7]), # penality on U-turns and places potentially already visited
    ([0.5, 1]), # penality only on U-turns
])
def test_UNIT_balance_and_momentum_overflow_robust(momentum_params):
    """
    Check that the algorithm is robust to very high values of pheromones (NaN).
    """
    position = 2
    position_historic = 1
    pheromoneLevels = 1.0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    adjacencyMat = [[0, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [1, 2, 5]
    param_balance = 10000
    
    neighbourhood = [1, 3, 4]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)
    assert not any(np.isnan(balanced_direction))
    assert sum(balanced_direction) == pytest.approx(1)

def test_UNIT_balance_and_momentum_exponential():
    """
    Check that the algorithm is robust to very high values of pheromones (NaN).
    """
    position = 2
    position_historic = 1
    pheromoneLevels = 0.0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    adjacencyMat = [[0, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [0.1, 0.2, 0, 0.1]
    param_balance = 5.5
    
    neighbourhood = [0, 1, 3, 4]
    momentum_params = [1, 1]

    check = [0.161084, 0.637101, 0.040731, 0.161084]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)
    assert balanced_direction == pytest.approx(check, rel=1e-3)
    assert sum(balanced_direction) == pytest.approx(1)

def test_UNIT_balance_and_momentum_stochastic():
    """
    Check that the probabilities are uniform when pheromone levels are equal everywhere and no momentum penalty is applied.
    """
    position = 2
    position_historic = 1
    pheromoneLevels = 0.0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    
    adjacencyMat = [[0, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [2, 2, 2]
    param_balance = 5.5
    
    neighbourhood = [1, 3, 4]
    momentum_params = [1, 1]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)
    assert balanced_direction == pytest.approx([1/3, 1/3, 1/3])
    assert sum(balanced_direction) == pytest.approx(1)

def test_UNIT_balance_and_momentum_null_param_stochastic():
    """
    Check that the probabilities are uniform when the param_balance is null, pheromone levels are equal everywhere and no momentum penalty is applied.
    """
    position = 2
    position_historic = 1
    pheromoneLevels = 1.0
    grid = [MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels), MockPlaceAgent(pheromoneLevels)]
    
    adjacencyMat = [[0, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0],
                    [0, 1, 0, 1, 1],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 0, 0]]
    ag_ant = MockAnt(position, position_historic, grid, adjacencyMat)
    
    unified_pheromone = [1, 1, 1]
    param_balance = 0
    
    neighbourhood = [1, 3, 4]
    momentum_params = [1, 1]

    balanced_direction = BalanceDirectionWithMomentum(unified_pheromone, ag_ant, neighbourhood, param_balance, momentum_params)
    check = [1/3, 1/3, 1/3]
    assert balanced_direction == pytest.approx(check)
    assert sum(balanced_direction) == pytest.approx(1)