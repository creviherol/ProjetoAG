import math
from genetic_algorithm_tsp import GeneticAlgorithmTSP

class Graph:
    def __init__(self, size, directed): #Passo6
       
        self.size = size
        self.edges = {} 
        self.nodes = {}  
        self.start_city = None  
        self.directed = directed  

    def add_edge(self, a, b, weight=1): #Passo10

        self.edges.setdefault(a, []).append((b, weight))
        if not self.directed:
            self.edges.setdefault(b, []).append((a, weight))

    def add_node(self, a, x, y): #Passo8
        
        if a not in self.edges:
            self.nodes[a] = (x, y) 
            distances = {key: self.euclidean_distance(a, key) for key in self.nodes if key != a}
            for key, distance in distances.items():
                self.add_edge(a, key, distance)
        

    def euclidean_distance(self, a, b): #Passo9
        
        x1, y1 = self.nodes[a]
        x2, y2 = self.nodes[b]
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return round(distance, 2)

    def vertices(self):
       
        return list(self.edges.keys())

    def getPathCost(self, path, incl_return_distance=False):
      
        pairs = zip(path, path[1:])
        cost = sum(self.euclidean_distance(city1, city2) for city1, city2 in pairs)

        if incl_return_distance:
           
            cost += self.euclidean_distance(path[0], path[-1])

        return cost
