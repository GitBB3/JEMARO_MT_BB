import pytest
import numpy as np
from src.environment import Environment
from src.pheromone import Pheromone

###########
## Tests ##
###########

def test_UNIT_environment_spawn_targets_obstacles():
    """
    Check that SpawnTargets raises an error if it tries to spawn a target on a placeAgent already occupied.
    """
    adj_mat = np.array([[0, 1], [1, 0]])

    lst_semantics = [["RThreat"], [0]]
    lst_diffusion = [0.3]
    lst_evaporation = [ 0.1]
    pheromone = Pheromone(lst_semantics, lst_diffusion, lst_evaporation, id)
    
    env = Environment(adj_mat, pheromone)

    ## Check SpawnTargets
    env.grid[0].type = "obstacle"
    targets = [1, 0]

    with pytest.raises(ValueError):
        env.SpawnTargets(targets)
    
    ## Check SpawnObstacles
    env.grid[1].type = "target"
    obstacles = [1]

    with pytest.raises(ValueError):
        env.SpawnObstacles(obstacles)
