import numpy as np

from placeAgent import placeAgent


# For an hexagonal environment
class Environment:
    def __init__(self, adjacencyMat):
        self.adjacencyMat = adjacencyMat # adjacency matrix between the hexagonal cells of the environment grid
        self.grid = [placeAgent(i,i) for i in range (len(adjacencyMat))] # environment hexagonal grid
    def env_generator(self):
        size = len(self.adjacencyMat)
        M = np.random.randint(0, 2, size=(size, size)) # random matrix full of 0 and 2
        upper_triangle = np.triu(M, k=1)
        new_adjacencyMat = upper_triangle + upper_triangle.T
        self.adjacencyMat = new_adjacencyMat