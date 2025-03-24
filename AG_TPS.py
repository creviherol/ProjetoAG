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
    

    def calculo_diverciade_genetica(self, populacao):#Passo 33
        
        matrix_rota = np.array([list(rota) for rota in populacao])
        distancia_pares = np.sum(matrix_rota[:, None, :] != matrix_rota[None, :, :], axis=2)
        distancia_total = np.sum(distancia_pares)
        numero_pares = len(populacao) * (len(populacao) - 1)
        average_distance = distancia_total / numero_pares
        divercidade_genetica = 1 / (1 + average_distance)

        return divercidade_genetica

    def obter_divercidade_genetica(self):#Passo36
    
        return self.valor_divercidade_genetica

    def indice_custo_minimo(self, costs):#Passo32

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
            #nova população criada para a nova geração
            indice_aptidao, rota_apta, aptdao_apta = self.obter_rota_adequada(grafo, populacao)
            rota_apta = [list(OrderedDict(self.Pont_mapeado).values())[
                    list(OrderedDict(self.Pont_map).values()).index(char)] if char in list(
                    OrderedDict(self.Pont_map).values()) else char for char in rota_apta]
            #calcula entre todas as rotas a mais apta
           
            divercidade_genetica = self.calculo_diverciade_genetica(populacao)
            self.valor_divercidade_genetica.append(round(divercidade_genetica, 4))
            #Adiciona a divicidade dessa geração para a lista de divercidade com 4 casas 
            if self.converged(populacao):
                print("Convergiu", populacao)
                print('\nConvergiu em um lugar minimo.')
                break #Analisa se a população convergiu
        return rota_apta, aptdao_apta

    def criar_nova_geracao(self, grafo, populacao, numero_de_transferencia): #Passo16
       
        nova_populacao = self.add_rotas_aptas(grafo, populacao, numero_de_transferencia)
        nova_populacao += [self.mutacao(self.crossover(*self.selecao_parentes(grafo, populacao))) for _ in
                           range(self.tamanho_populacao - numero_de_transferencia)]
        return nova_populacao

    def add_rotas_aptas(self, grafo, populacao, numero_de_transferencia): #Passo17
       
        sorted_population = [x for _, x in sorted(zip(self.calcular_aptidao(grafo, populacao), populacao))]
        return sorted_population[:numero_de_transferencia]

    def obter_rota_adequada(self, grafo, populacao):#Passo30
        
        aptidao = self.calcular_aptidao(grafo, populacao)
        indice_aptidao = self.indice_custo_minimo(aptidao)
        return indice_aptidao, populacao[indice_aptidao], aptidao[indice_aptidao]

    def selecao_parentes(self, grafo, populacao):#Passo21
       #seleciona os individos
        return self.selecao_torneio(grafo, populacao), self.selecao_torneio(grafo, populacao)

    def Pont_randomico(self, nos_grafo):#Passo15
        
        nos = [no for no in nos_grafo if no != self.grafo.Pont_inicial and no != self.grafo.pent_point]
        #cria uma lista com os caracteres dos pontos com exceção do ponto inicial e do penutimo que deseja passar 
        return [
            self.grafo.Pont_inicial + ''.join(rd.sample(nos, len(nos))) + self.grafo.pent_point + self.grafo.Pont_inicial
            for _ in range(self.tamanho_populacao)
        ]

    def calcular_aptidao(self, grafo, populacao):#Passo18/Passo31
        
        return [grafo.obter_custo_caminho(caminho) for caminho in populacao]

    def selecao_torneio(self, grafo, populacao):#Passo22
        
        competidores_torneio = rd.choices(populacao, k=self.tamanho_torneio)
        return min(competidores_torneio, key=lambda caminho: grafo.obter_custo_caminho(caminho))

    def crossover(self, parent1, parent2):#Passo24
        
        comprimento_prole = len(parent1) - 3 
        #valor de quantidades de genes menos os 2 de inicio e o penutimo
        filhos = ['' for _ in range(comprimento_prole)]
        #Cria uma lista com um numeros de espaço igual o comprimento da prole
        indice_baixo, indice_alto = self.calcular_indice_2Pont(parent1)
        #Gera dois pontos de rupitura para crosover do individo
        filhos[indice_baixo: indice_alto ] = list(parent1)[indice_baixo: indice_alto ]
        #pega os genes na lista com os genes do parente1 em relação aos pontos gerados
        indice_lugar_vazio = [i for i in range(comprimento_prole) if filhos[i] == '']
        for i in parent2[1: -2]:
            #preenche os pontos não preenchidos com os genes do parente2  
            if '' not in filhos or not indice_lugar_vazio:
                break
            if i not in filhos:
                filhos[indice_lugar_vazio.pop(0)] = i
        
        filhos = [self.grafo.Pont_inicial] + filhos + [self.grafo.pent_point] +[self.grafo.Pont_inicial]
    
        return ''.join(filhos)


    def mutacao(self, genome):#Passo26
        
        if rd.random() < self.taxa_mutacao:
            #Se a probabilidade de mutação for atendida ele executa 
            indice_baixo, indice_alto = self.calcular_indice_2Pont(genome)
            return self.troca(indice_baixo, indice_alto, genome)
        else:
            return genome

    def calcular_indice_2Pont(self,parent):#Passo25/PASSO28
        
        indice_baixo = rd.randint(1, len(parent) - 3)
        #Calcula um ponto entre 1 e o numero de pontos do problema -3
        indice_alto = rd.randint(indice_baixo, len(parent) - 3)
        #Calcula um segundo ponto o valor anterio e o numero de pontos do problema -3
        if indice_alto - indice_baixo > math.ceil(len(parent) // 2):
              #Se o diferença de os indices for maior 
              return self.calcular_indice_2Pont(parent)
        else:
              return indice_baixo, indice_alto

    def troca(self, indice_baixo, indice_alto, genome):#Passo29
        
        genome = list(genome)
        #print(genome)
        genome[indice_baixo], genome[indice_alto] = genome[indice_alto], genome[indice_baixo]
        #ele troca dois pontos de lugar para assim ocorrer a mutação
        #print(genome)
        return ''.join(genome)

    def converged(self, populacao):#Passo34
        
        return all(genome == populacao[0] for genome in populacao)
    
    def Bloco_notas (texto):
        with open("meu_arquivo.txt", "a") as arquivo:
            arquivo.writelines(texto + "\n")