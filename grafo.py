import math
from AG_TPS import EXE_AG_TSP

class Graph:
    def __init__(self, tamanho): #Passo6
       
        self.tamanho = tamanho
        self.bordas = {} 
        self.nos = {}  
        self.Pont_inicial = None  
        #Atribui valor as variaveis 

    def add_borda(self, a, b, peso): #Passo10

        self.bordas.setdefault(a, []).append((b, peso))
        """
        Adiciona ao dicionario bordas uma palavra chave referente
        a variavel a e adiciona dentro dela um outra ponto e sua 
        distancia referente de a para b
        """
        self.bordas.setdefault(b, []).append((a, peso))
        #mesma coisa de cima so que agora de b para a

    def add_no(self, a, x, y): #Passo8
        
        if a not in self.bordas:#Executara quando a não fizer parte de bordas
            self.nos[a] = (x, y) 
            #Adicio as cordenas de cada ponto com seu caractere no dicionario nos
            distancias = {key: self.distancia_euclidiana(a, key) for key in self.nos if key != a}
            """
            Adiciona ao dicionario de distancias key que sera os pontos as quando key não pode ser
            igual a variavel a para não criar a distancia de um ponto para ele mesmo, depois dos :
            vamos para variavel que calcula a distancia de 2 pontos.
            """
            for key, distancia in distancias.items():
                """
                Sera um loop com uma quantidade de vezes igual a quantidades de bordas que o 
                problema tera que sera Soma triangular do numero de pontos - 1
                """
                self.add_borda(a, key, distancia)#adiciona as bordas do grafo   

    def distancia_euclidiana(self, a, b): #Passo9/Passo20
        x1, y1 = self.nos[a] 
        #pega as cordenada de um dos pontos e coloca seu valor em x1 e x2
        x2, y2 = self.nos[b]
        distancia = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        #Calcula a distancia de 2 pontas atravez da teorema de pitagoras 
        return round(distancia, 2) #Aredonda para 2 casas apos a virgula

    def vertices(self):
       
        return list(self.bordas.keys())

    def getPathCost(self, path, incl_return_distance=True): #Passo19
      
        pairs = zip(path, path[1:])
        cost = sum(self.distancia_euclidiana(city1, city2) for city1, city2 in pairs)

        if incl_return_distance:
           
            cost += self.distancia_euclidiana(path[0], path[-1])

        return cost
