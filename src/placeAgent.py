class placeAgent():
    def __init__(self, id_place, pheromone, type):
        self.id = id_place
        # self.position = position # not needed right? cause the position is only determined relatively to adjacency with other placeAgents
        self.pheromone = pheromone
        self.pheromoneLevels = [0.0 for _ in range (len(pheromone.semantics))]
        self.type = type
        self.timestamp = 0
    
    def aggregation(self, amount):
        for i in range (len(amount)):
            self.pheromoneLevels[i] += amount[i]
    
    def evaporation(self):
        for i in range (len(self.pheromoneLevels)):
            self.pheromoneLevels[i] *= (1-self.pheromone.evaporation[i])

    def TimeUpdate(self, time):
        self.timestamp = time