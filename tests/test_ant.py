import pytest
from src.pathPlanning import SelectGuidance, BalanceDirection, MomentumAddition

###########
## Mocks ##
###########

class MockPlaceAgent:
    def __init__(self, pheromoneLevels):
        self.pheromoneLevels = pheromoneLevels

class MockEnvironment:
    def __init__(self, grid):
        self.grid = grid

class MockPheromone:
    def __init__(self, dynamics):
        self.dynamics = dynamics

class MockAnt:
    def __init__(self, position, grid, dynamics):
        self.memory = MockEnvironment(grid)
        self.pheromone = MockPheromone(dynamics)
        self.position = position

###########
## Tests ##
###########

def test_select_guidance_no_bi_dynamics():
    """
    Check if a pheromone semantic with only one dynamic is added in the list of pheromones.
    The id of every pheromone semantic whose dynamic is "False" should be in the result of the function "SelectGuidance".
    """
    position = 0
    grid = []
    dynamics = [0, 0, 0]
    ag_ant = MockAnt(position, grid, dynamics)

    neighbourhood = []

    guid_idx = SelectGuidance(ag_ant, neighbourhood)
    assert guid_idx == [0, 1, 2]

def test_select_guidance_null_levels():
    """
    Check that a grid place with null level of pheromones and one double dynamic semantic selects the long_range dynamic.
    """
    position = 0
    pheromoneLevels = [0, 0]
    grid = [MockPlaceAgent(pheromoneLevels)]
    dynamics = [1, 1]
    ag_ant = MockAnt(position, grid, dynamics)

    neighbourhood = []

    guid_idx = SelectGuidance(ag_ant, neighbourhood)
    assert guid_idx == [1]