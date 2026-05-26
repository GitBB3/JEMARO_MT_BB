from placeAgent import placeAgent


# For an hexagonal environment
class Environment:
    def __init__(self, adjacencyMat):
        self.adjacencyMat = adjacencyMat # adjacency matrix between the hexagonal cells of the environment grid
        self.grid = [placeAgent(i,i) for i in range (len(adjacencyMat))] # environment hexagonal grid