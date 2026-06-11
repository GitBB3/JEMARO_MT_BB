import pytest
import numpy as np
from src.pathPlanning import BalanceDirection

###########
## Mocks ##
###########



###########
## Tests ##
###########

def test_UNIT_balance_direction_uniform_balance():
    """
    Check that in absence of pheromones in the neighbourhood of the agent, it moves stochastically.
    """
    unified_pheromone = [0, 0, 0, 0, 0]
    param_balance = 5.5

    balanced_direction = BalanceDirection(unified_pheromone, param_balance)
    assert balanced_direction == [1/5, 1/5, 1/5, 1/5, 1/5]

def test_UNIT_balance_direction_exponential_weight_balance():
    """
    Check that in presence of pheromones in the neighbourhood of the agent, the probability to move to another placeAgent is exponentially weighted.
    """
    unified_pheromone = [0.1, 0.2, 0, 0.2, 0.1]
    param_balance = 5.5

    weights = [1/6, 2/6, 0, 2/6, 1/6]
    sum_w = np.sum(np.exp(np.array(weights)*param_balance))
    check = [np.exp(param_balance*wt)/sum_w for wt in weights]
    
    balanced_direction = BalanceDirection(unified_pheromone, param_balance)
    assert balanced_direction == pytest.approx(check) # acceptance of a difference at 10-6

def test_UNIT_balance_direction_high_values():
    """
    Check that the system avoids overflows in case of high pheromone values of high balance parameter.
    """
    unified_pheromone = [0.1, 0.2, 0, 0.2, 0.1]
    param_balance = 10000 # exagerated parameter for numerical explosion / overflow
    
    balanced_direction = BalanceDirection(unified_pheromone, param_balance)
    assert not any(np.isnan(balanced_direction))

def test_UNIT_balance_direction_null_parameter():
    """
    Check that the system avoids overflows in case of high pheromone values of high balance parameter.
    """
    unified_pheromone = [0.1, 0.2, 0, 0.2, 0.1]
    param_balance = 0 # if param_balance had to be null
    
    balanced_direction = BalanceDirection(unified_pheromone, param_balance)
    assert balanced_direction == [1/5, 1/5, 1/5, 1/5, 1/5]

@pytest.mark.parametrize("set_unified_pheromone, set_param_balance", [
    ([0, 0, 0, 0, 0], 5.5),
    ([0.1, 0.2, 0, 0.2, 0.1], 5.5),
    ([0.1, 0.2, 0, 0.2, 0.1], 10000),
    ([0.1, 0.2, 0, 0.2, 0.1], 0),
])
def test_UNIT_balance_direction_coherent_probabilities(set_unified_pheromone, set_param_balance):
    """
    Check that the sum of probabilities is always 1.
    """

    balanced_direction = BalanceDirection(set_unified_pheromone, set_param_balance)
    assert sum(balanced_direction) == pytest.approx(1.0)