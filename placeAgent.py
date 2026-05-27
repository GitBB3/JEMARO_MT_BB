class placeAgent():
    def __init__(self, id_place, position, evaporation_rate_u, evaporation_rate_e, diffusion_rate_u, diffusion_rate_e):
        self.id = id_place
        # self.position = position # not needed right? cause the position is only determined relatively to adjacency with other placeAgents
        self.evaporation_rate_u = evaporation_rate_u
        self.evaporation_rate_e = evaporation_rate_e
        self.diffusion_rate_u = diffusion_rate_u
        self.diffusion_rate_e = diffusion_rate_e
        self.uncertaintyPheromone = 0.0
        self.entropyPheromone = 0.0
    
    def aggregation(self, amount):
        self.uncertaintyPheromone += amount[0]
        self.entropyPheromone += amount[1]
    
    def evaporation(self):
        self.uncertaintyPheromone *= (1-self.evaporation_rate_u)
        self.entropyPheromone *= (1-self.evaporation_rate_e)