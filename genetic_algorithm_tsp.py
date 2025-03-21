import random as rd
import math
import numpy as np
from collections import OrderedDict

class GeneticAlgorithmTSP: #Passo12

    def __init__(self, graph, city_names, generations=20, population_size=10, tournament_size=4, mutationRate=0.1, fitness_selection_rate=0.1):

        self.graph = graph
        self.population_size = population_size
        self.generations = generations
        self.tournament_size = tournament_size
        self.mutationRate = mutationRate
        self.fitness_selection_rate = fitness_selection_rate

        self.genetic_diversity_values = []

        self.city_map = OrderedDict((char, city) for char, city in zip(range(32, 127), graph.vertices()))
        self.city_mapping = {char: city for char, city in zip(range(32, 127), city_names)}
        self.city_map[32], self.city_map[33] = self.city_map[33], self.city_map[32]

    def calculate_genetic_diversity(self, population):
        
        routes_matrix = np.array([list(route) for route in population])

        pairwise_distances = np.sum(routes_matrix[:, None, :] != routes_matrix[None, :, :], axis=2)

        total_distance = np.sum(pairwise_distances)
        num_pairs = len(population) * (len(population) - 1)
        average_distance = total_distance / num_pairs
        genetic_diversity = 1 / (1 + average_distance)

        return genetic_diversity

    def get_genetic_diversity_values(self):
    
        return self.genetic_diversity_values

    def minCostIndex(self, costs):

        return min(range(len(costs)), key=costs.__getitem__)

    def find_fittest_path(self, graph):#Passo14
        
        population = self.randomizeCities(graph.vertices())
        number_of_fits_to_carryover = math.ceil(self.population_size * self.fitness_selection_rate)

        if number_of_fits_to_carryover > self.population_size:
            raise ValueError('Fitness rate must be in [0, 1].')

        print('Optimizing TSP Route for Graph:')

        for generation in range(1, self.generations + 1):
            
            new_population = self.create_next_generation(graph, population, number_of_fits_to_carryover)
            population = new_population

            fittest_index, fittest_route, fittest_fitness = self.get_fittest_route(graph, population)
            fittest_route = [list(OrderedDict(self.city_mapping).values())[
                                 list(OrderedDict(self.city_map).values()).index(char)] if char in list(
                OrderedDict(self.city_map).values()) else char for char in fittest_route]
           
            genetic_diversity = self.calculate_genetic_diversity(population)
            self.genetic_diversity_values.append(round(genetic_diversity, 4))
            
            if self.converged(population):
                print("Converged", population)
                print('\nConverged to a local minima.')
                break

        return fittest_route, fittest_fitness

    def create_next_generation(self, graph, population, number_of_fits_to_carryover): #Passo16
       
        new_population = self.add_fittest_routes(graph, population, number_of_fits_to_carryover)
        new_population += [self.mutate(self.crossover(*self.select_parents(graph, population))) for _ in
                           range(self.population_size - number_of_fits_to_carryover)]
        return new_population

    def add_fittest_routes(self, graph, population, number_of_fits_to_carryover): #Passo17
       
        sorted_population = [x for _, x in sorted(zip(self.computeFitness(graph, population), population))]
        return sorted_population[:number_of_fits_to_carryover]

    def get_fittest_route(self, graph, population):
        
        fitness = self.computeFitness(graph, population)
        fittest_index = self.minCostIndex(fitness)
        return fittest_index, population[fittest_index], fitness[fittest_index]

    def select_parents(self, graph, population):#Passo21
       
        return self.tournamentSelection(graph, population), self.tournamentSelection(graph, population)

    def randomizeCities(self, graph_nodes):#Passo15
        
        nodes = [node for node in graph_nodes if node != self.graph.start_city and node != self.graph.pent_point]

        return [
            self.graph.start_city + ''.join(rd.sample(nodes, len(nodes))) + self.graph.pent_point + self.graph.start_city
            for _ in range(self.population_size)
        ]

    def computeFitness(self, graph, population):#Passo18
        
        return [graph.getPathCost(path) for path in population]

    def tournamentSelection(self, graph, population):#Passo22
        
        tournament_contestants = rd.choices(population, k=self.tournament_size)
        return min(tournament_contestants, key=lambda path: graph.getPathCost(path))

    def crossover(self, parent1, parent2):#Passo23
        
        offspring_length = len(parent1) - 3 

        offspring = ['' for _ in range(offspring_length)]
        
        index_low, index_high = self.computeTwoPointIndexes(parent1)
        offspring[index_low: index_high ] = list(parent1)[index_low: index_high ]
        empty_place_indexes = [i for i in range(offspring_length) if offspring[i] == '']
        for i in parent2[1: -2]:  
            if '' not in offspring or not empty_place_indexes:
                break
            if i not in offspring:
                offspring[empty_place_indexes.pop(0)] = i
        
        offspring = [self.graph.start_city] + offspring + [self.graph.pent_point] +[self.graph.start_city]
    
        return ''.join(offspring)


    def mutate(self, genome):
        
        if rd.random() < self.mutationRate:
            index_low, index_high = self.computeTwoPointIndexes(genome)
            return self.swap(index_low, index_high, genome)
        else:
            return genome

    def computeTwoPointIndexes(self,parent):#Passo24
        
        index_low = rd.randint(1, len(parent) - 3)
        index_high = rd.randint(index_low, len(parent) - 3)

        if index_high - index_low > math.ceil(len(parent) // 2):
              return self.computeTwoPointIndexes(parent)
        else:
              return index_low, index_high

    def swap(self, index_low, index_high, string):
        
        string = list(string)
        string[index_low], string[index_high] = string[index_high], string[index_low]
        return ''.join(string)

    def converged(self, population):
        
        return all(genome == population[0] for genome in population)
    
    def Bloco_notas (texto):
        with open("meu_arquivo.txt", "a") as arquivo:
            arquivo.writelines(texto + "\n")