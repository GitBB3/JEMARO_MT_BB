class placeAgent():
    def __init__(self, id_agent, position):
        self.id = id_agent
        self.position = position
        self.uncertaintyPheromone = 0.0
        self.entropyPheromone = 0.0
    
    def aggregation(self, amount):
        pass
    
    def evaporation(self, amount):
        pass
    
    def diffusion(self, adjacencyMatrix):
        pass