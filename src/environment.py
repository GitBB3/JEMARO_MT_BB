import numpy as np

from src.placeAgent import placeAgent


# For an hexagonal environment
class Environment: # TODO: check dependencies with pheromone class
    def __init__(self, adjacencyMat, pheromone):
        self.adjacencyMat = adjacencyMat # adjacency matrix between the hexagonal cells of the environment grid
        self.grid = [placeAgent(i,pheromone) for i in range (len(adjacencyMat))] # environment hexagonal grid
    
    def env_generator(self):
        size = len(self.adjacencyMat)
        M = np.random.randint(0, 2, size=(size, size)) # random matrix full of 0 and 2
        upper_triangle = np.triu(M, k=1)
        new_adjacencyMat = upper_triangle + upper_triangle.T
        self.adjacencyMat = new_adjacencyMat
    
    def diffusion(self):
        diff_map = [[0.0, 0.0] for i in range (len(self.grid))]
        for a in self.grid:
            idx_neighbours = [idx for idx, adjacency in enumerate(self.adjacencyMat[a.id]) if adjacency]
            diff_u = a.uncertaintyPheromone * a.diffusion_rate_u / 6 # Diffusion on an hexagonal grid without border effects (open environment)
            diff_e = a.entropyPheromone * a.diffusion_rate_e / 6
            for idx in idx_neighbours:
                diff_map[idx][0] += diff_u
                diff_map[idx][1] += diff_e
        for a in self.grid:
            a.uncertaintyPheromone = a.uncertaintyPheromone*(1 - a.diffusion_rate_u) + diff_map[a.id][0]
            a.entropyPheromone = a.entropyPheromone*(1 - a.diffusion_rate_e) + diff_map[a.id][1]