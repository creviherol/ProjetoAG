import re
from grafo import Graph
from AG_TPS import EXE_AG_TSP
from plot import plot_tsp_path, plot_genetic_diversity
from collections import OrderedDict

with open("meu_arquivo.txt", "w") as arquivo:
    pass  # Não escreve nada, só apaga o conteúdo

def main():
    with open('Pont_de_interece.txt', 'r') as file: #Passo1
        Pont_Data = file.read() #Le o arquivo Pont_de_interece e coloca na variavel Pont_Data

    Pont_modulo = re.compile(r'(\w+):\s\((\d+),\s(\d+)\)') #Passo2
    #Orgazisa um metodo de compilar os pontos de interese 

    Ponts = Pont_modulo.findall(Pont_Data) #Passo3 
    #Usa o metodo criado para organizar os pontos de interese

    Pont_mapeamento = OrderedDict((Pont[0], chr(i + 33)) for i, Pont in enumerate(Ponts)) #Passo4
    """
    cria um dicionario de pares com o primeiro valor sendo dos modulos de Ponts que no caso seram
    o nome do ponto e uma função que coloca cada ponto um um um unicode para a criação do cromossomo
    sendo começando pelo unicode 33   
    """

    Pont_grafo = Graph(len(Ponts)) #Passo5
    #Coloca o valor de tamanho como quantos pontos existe

    for Pont, x, y in Ponts: #Passo7
        Pont_grafo.add_no(Pont_mapeamento[Pont], int(x), int(y))
        """"
        Manda os parametros dos caracteres do gene e os pontos no mapa x e y
        e repete o loop um numero de vezes igual o numero de pontos 
        """

    Pont_grafo.Pont_inicial = Pont_mapeamento['Recepcao'] #Defini a cidade inicial
    Pont_grafo.pent_point = Pont_mapeamento['Refeitorio'] #Defini a cidade que deve passar antes de ir para o final

    AG_TSP = EXE_AG_TSP( #Passo11
        grafo=Pont_grafo,
        Pont_nomes=[Pont for Pont, _, _ in Ponts],
        #lista dos nomes das cidades 
        geracoes=10,
        tamanho_populacao=15,
        tamanho_torneio=5,
        taxa_mutacao=0.1,
        taxa_de_aptidao=0.5,
        #Declara alguns parametros para excução do TPS
    )

    caminho_apto, custo_caminho = AG_TSP.menor_caminho(Pont_grafo)#Passo13

    genetic_diversity_values = AG_TSP.obter_divercidade_genetica()#Passo35

    formatacao_caminho = ' -> '.join(caminho_apto)
    print('\nCaminho: {0}\nCusto: {1}'.format(formatacao_caminho, custo_caminho))

    coordinates_dict = {Pont: (int(x), int(y)) for Pont, x, y in Ponts}

    coordinates_list = [coordinates_dict[Pont] for Pont in caminho_apto]

    plot_tsp_path(caminho_apto, coordinates_list, 'fabrica.png', custo_caminho)

    plot_genetic_diversity(genetic_diversity_values)


if __name__ == "__main__":
    main() #Inicia a função main quando o nome do modulo de execução for __main__

