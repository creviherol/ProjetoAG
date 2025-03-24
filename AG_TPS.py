import random as rd
import math
import numpy as np
from collections import OrderedDict

class EXE_AG_TSP: #Passo12

    def __init__(self, grafo, Pont_nomes, geracoes=20, tamanho_populacao=10, tamanho_torneio=4, taxa_mutacao=0.1, taxa_de_aptidao=0.1):

        self.grafo = grafo
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.tamanho_torneio = tamanho_torneio
        self.taxa_mutacao = taxa_mutacao
        self.taxa_de_apitidao = taxa_de_aptidao
        self.valor_divercidade_genetica = []
        self.Pont_map = OrderedDict((char, Pont) for char, Pont in zip(range(32, 127), grafo.vertices()))
        #Cria um dicionario de pares dos caracteres do problea e numeros de 32 ate 127 conforma o numero de pontos
        self.Pont_mapeado = {char: Pont for char, Pont in zip(range(32, 127), Pont_nomes)}
        #Cria um dicionario de pares dos numeros de 32 a 127 referentes a cada ponto
    

    def calculate_genetic_diversity(self, populacao):
        
        routes_matrix = np.array([list(route) for route in populacao])

        pairwise_distances = np.sum(routes_matrix[:, None, :] != routes_matrix[None, :, :], axis=2)

        total_distance = np.sum(pairwise_distances)
        num_pairs = len(populacao) * (len(populacao) - 1)
        average_distance = total_distance / num_pairs
        genetic_diversity = 1 / (1 + average_distance)

        return genetic_diversity

    def get_genetic_diversity_values(self):
    
        return self.valor_divercidade_genetica

    def minCostIndex(self, costs):

        return min(range(len(costs)), key=costs.__getitem__)

    def menor_caminho(self, grafo):#Passo14
        
        populacao = self.Pont_randomico(grafo.vertices())
        #cria a população inicial
        numero_de_transferencia = math.ceil(self.tamanho_populacao * self.taxa_de_apitidao)
        #numeros de melhores individos que continuaram no conjunto solução 
        if numero_de_transferencia > self.tamanho_populacao:
            raise ValueError('A taxa de aptidão deve estar em [0, 1].')
        #Avalia se o numero de melhores individos que ficaram e maior que a população
        print('Otimizando a rota:')

        for geracao in range(1, self.geracoes + 1):
            
            nova_populacao = self.criar_nova_geracao(grafo, populacao, numero_de_transferencia)
            populacao = nova_populacao

            indice_aptidao, rota_apta, aptdao_apta = self.obter_rota_adequada(grafo, populacao)
            rota_apta = [list(OrderedDict(self.Pont_mapeado).values())[
                                 list(OrderedDict(self.Pont_map).values()).index(char)] if char in list(
                OrderedDict(self.Pont_map).values()) else char for char in rota_apta]
           
            genetic_diversity = self.calculate_genetic_diversity(populacao)
            self.valor_divercidade_genetica.append(round(genetic_diversity, 4))
            
            if self.converged(populacao):
                print("Convergiu", populacao)
                print('\nConvergiu em um lugar minimo.')
                break

        return rota_apta, aptdao_apta

    def criar_nova_geracao(self, grafo, populacao, numero_de_transferencia): #Passo16
       
        nova_populacao = self.add_rotas_aptas(grafo, populacao, numero_de_transferencia)
        nova_populacao += [self.mutate(self.crossover(*self.select_parents(grafo, populacao))) for _ in
                           range(self.tamanho_populacao - numero_de_transferencia)]
        return nova_populacao

    def add_rotas_aptas(self, grafo, populacao, numero_de_transferencia): #Passo17
       
        sorted_population = [x for _, x in sorted(zip(self.computeFitness(grafo, populacao), populacao))]
        return sorted_population[:numero_de_transferencia]

    def obter_rota_adequada(self, grafo, populacao):
        
        fitness = self.computeFitness(grafo, populacao)
        indice_aptidao = self.minCostIndex(fitness)
        return indice_aptidao, populacao[indice_aptidao], fitness[indice_aptidao]

    def select_parents(self, grafo, populacao):#Passo21
       
        return self.tournamentSelection(grafo, populacao), self.tournamentSelection(grafo, populacao)

    def Pont_randomico(self, nos_grafo):#Passo15
        
        nos = [no for no in nos_grafo if no != self.grafo.Pont_inicial and no != self.grafo.pent_point]
        #cria uma lista com os caracteres dos pontos com exceção do ponto inicial e do penutimo que deseja passar 
        return [
            self.grafo.Pont_inicial + ''.join(rd.sample(nos, len(nos))) + self.grafo.pent_point + self.grafo.Pont_inicial
            for _ in range(self.tamanho_populacao)
        ]

    def computeFitness(self, grafo, populacao):#Passo18
        
        return [grafo.getPathCost(path) for path in populacao]

    def tournamentSelection(self, grafo, populacao):#Passo22
        
        tournament_contestants = rd.choices(populacao, k=self.tamanho_torneio)
        return min(tournament_contestants, key=lambda path: grafo.getPathCost(path))

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
        
        offspring = [self.grafo.Pont_inicial] + offspring + [self.grafo.pent_point] +[self.grafo.Pont_inicial]
    
        return ''.join(offspring)


    def mutate(self, genome):
        
        if rd.random() < self.taxa_mutacao:
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

    def converged(self, populacao):
        
        return all(genome == populacao[0] for genome in populacao)
    
    def Bloco_notas (texto):
        with open("meu_arquivo.txt", "a") as arquivo:
            arquivo.writelines(texto + "\n")