import numpy as np

from src.placeAgent import placeAgent


# For an hexagonal environment
class Environment:
    def __init__(self, adjacencyMat, pheromone, nest_position):
        self.adjacencyMat = adjacencyMat # adjacency matrix between the hexagonal cells of the environment grid
        self.grid = [placeAgent(i, pheromone, "basic") for i in range (len(adjacencyMat))] # environment hexagonal grid
        self.nest_position = nest_position

    def env_generator(self):
        size = len(self.adjacencyMat)
        M = np.random.randint(0, 2, size=(size, size)) # random matrix full of 0 and 2
        upper_triangle = np.triu(M, k=1)
        new_adjacencyMat = upper_triangle + upper_triangle.T
        self.adjacencyMat = new_adjacencyMat
    
    def SpawnTargets(self, targets):
        """
        Spawns targets randomly or according to a list in parameters.

        :param targets: Number of targets to be spawned randomly if it is an integer OR list of the targets' positions.
        :type targets: int OR list[int]
        """
        if isinstance(targets, int):
            for i in range (targets):
                security = 50
                iter = 0
                spawned = False
                while not spawned and iter < security:
                    pos = np.random.randint(0, len(self.grid))
                    if self.grid[pos].type == "basic":
                        self.grid[pos].type = "target"
                        spawned = True
                    iter += 1
                if iter >= security: raise RuntimeError("Runtime error: took too much time to find an empty spot for the target.")

        else:
            for i in range (len(targets)):
                if self.grid[targets[i]].type == "basic":
                    self.grid[targets[i]].type = "target"
                else: raise ValueError(f"Conflict error: cannot spawn the target on position {targets[i]}, which is already of type '{self.grid[targets[i]].type}'.")

    def SpawnObstacles(self, obstacles):
        """
        Spawns obstacles randomly or according to a list in parameters.

        :param obstacles: Number of obstacles to be spawned randomly if it is an integer OR list of the obstacles' positions.
        :type obstacles: int OR list[int]
        """
        if isinstance(obstacles, int):
            for i in range (obstacles):
                security = 50
                iter = 0
                spawned = False
                while not spawned and iter < security:
                    pos = np.random.randint(0, len(self.grid))
                    if self.grid[pos].type == "basic":
                        self.grid[pos].type = "obstacle"
                        spawned = True
                    iter += 1
                if iter >= security: raise RuntimeError("Took too much time to find an empty spot for the obstacle.")

        else:
            for i in range (len(obstacles)):
                if self.grid[obstacles[i]].type == "basic":
                    self.grid[obstacles[i]].type = "obstacle"
                else: raise ValueError(f"Cannot spawn the obstacle on position {obstacles[i]}, which is already of type '{self.grid[obstacles[i]].type}'.")

    
    def diffusion(self):
        """
        Diffuse.
        """
        nb_places = len(self.grid)
        nb_phero_types = len(self.grid[0].pheromone.semantics)

        diff_map = [[0.0] * nb_phero_types for _ in range(nb_places)]
        for place in self.grid:
            idx_neighbours = [idx for idx, adjacency in enumerate(self.adjacencyMat[place.id]) if adjacency]
            nb_neighbours = len(idx_neighbours)
            
            if nb_neighbours == 0:
                continue
            for phero_idx in range(nb_phero_types):
                current_level = place.pheromoneLevels[phero_idx]
                diff_rate = self.grid[0].pheromone.diffusion[phero_idx]

                diff_amount = (current_level * diff_rate) / nb_neighbours

                for idx_neigh in idx_neighbours:
                    diff_map[idx_neigh][phero_idx] += diff_amount
        for place in self.grid:
            for phero_idx in range(nb_phero_types):
                diff_rate = self.grid[0].pheromone.diffusion[phero_idx]
                place.pheromoneLevels[phero_idx] = (place.pheromoneLevels[phero_idx] * (1.0 - diff_rate) + diff_map[place.id][phero_idx])
        
    def env_evaporation(self):
        for place in self.grid:
            place.evaporation()