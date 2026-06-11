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

def test_select_guidance_bidynamics_short():
    """
    Check that a grid place with more short range pheromone guidance will select the short range pheromone.
    """
    position = 0
    pheromoneLevels = [[0, 0],[0.2, 0]]
    grid = [MockPlaceAgent(pheromoneLevels[0]), MockPlaceAgent(pheromoneLevels[1])]
    dynamics = [1, 1]
    ag_ant = MockAnt(position, grid, dynamics)

    neighbourhood = [1]

    guid_idx = SelectGuidance(ag_ant, neighbourhood)
    assert guid_idx == [0]

def test_select_guidance_bidynamics_long():
    """
    Check that a grid place with more short range pheromone guidance will select the short range pheromone.
    """
    position = 0
    pheromoneLevels = [[0, 0],[0, 0.2]]
    grid = [MockPlaceAgent(pheromoneLevels[0]), MockPlaceAgent(pheromoneLevels[1])]
    dynamics = [1, 1]
    ag_ant = MockAnt(position, grid, dynamics)

    neighbourhood = [1]

    guid_idx = SelectGuidance(ag_ant, neighbourhood)
    assert guid_idx == [1]

def test_select_guidance_several_unidynamic():
    """
    Check that unidynamic semantics are considered as such.
    """
    position = 0
    pheromoneLevels = [[0.1,0.2,0.3],[0.1,0.2,0.3]]
    grid = [MockPlaceAgent(pheromoneLevels[0]), MockPlaceAgent(pheromoneLevels[1])]
    dynamics = [0, 0, 0]
    ag_ant = MockAnt(position, grid, dynamics)

    neighbourhood = [1]

    guid_idx = SelectGuidance(ag_ant, neighbourhood)
    assert guid_idx == [0, 1, 2]

def test_select_guidance_combination():
    """
    Check.
    """
    position = 0
    pheromoneLevels = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0.1,0.2,0.3, 0.4, 0.5, 0.7, 0.6, 0.8, 0.9, 1]]
    grid = [MockPlaceAgent(pheromoneLevels[0]), MockPlaceAgent(pheromoneLevels[1])]
    dynamics = [0, 1, 1, 0, 0, 3, 3, 2, 2, 0]
    ag_ant = MockAnt(position, grid, dynamics)

    neighbourhood = [1]

    guid_idx = SelectGuidance(ag_ant, neighbourhood)
    assert guid_idx == [0, 2, 3, 4, 6, 8, 9]