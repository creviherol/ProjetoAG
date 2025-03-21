import re
from graph import Graph
from genetic_algorithm_tsp import GeneticAlgorithmTSP
from plot import plot_tsp_path, plot_genetic_diversity
from collections import OrderedDict

with open("meu_arquivo.txt", "w") as arquivo:
    pass  # Não escreve nada, só apaga o conteúdo

def main():
    with open('cities.txt', 'r') as file: #Passo1
        cities_data = file.read() #Le o arquivo cidades e coloca na variavel cidade_data

    city_pattern = re.compile(r'(\w+):\s\((\d+),\s(\d+)\)') #Passo2

    cities = city_pattern.findall(cities_data) #Passo3
    GeneticAlgorithmTSP.Bloco_notas(str(cities) + "\n")

    city_mapping = OrderedDict((city[0], chr(i + 33)) for i, city in enumerate(cities)) #Passo4
    GeneticAlgorithmTSP.Bloco_notas(str(city_mapping) + "\n")

    germany_graph = Graph(len(cities), False) #Passo5
    #Cria um grafo com o numero de verticer 

    for city, x, y in cities: #Passo7
        germany_graph.add_node(city_mapping[city], int(x), int(y))

    germany_graph.start_city = city_mapping['A1'] #Defini a cidade inicial
    germany_graph.pent_point = city_mapping['A5'] #Defini a cidade que deve passar antes de ir para o final
    GeneticAlgorithmTSP.Bloco_notas(str(germany_graph.start_city) + "\n")
    GeneticAlgorithmTSP.Bloco_notas(str(germany_graph.pent_point) + "\n")


    ga_tsp_germany = GeneticAlgorithmTSP( #Passo11
        graph=germany_graph,
        city_names=[city for city, _, _ in cities], 
        generations=5,
        population_size=10,
        tournament_size=5,
        mutationRate=0.1,
        fitness_selection_rate=0.5,
    )

    fittest_path, path_cost = ga_tsp_germany.find_fittest_path(germany_graph) #Passo13

    genetic_diversity_values = ga_tsp_germany.get_genetic_diversity_values()

    formatted_path = ' -> '.join(fittest_path)
    print('\nPath: {0}\nCost: {1}'.format(formatted_path, path_cost))

    coordinates_dict = {city: (int(x), int(y)) for city, x, y in cities}

    coordinates_list = [coordinates_dict[city] for city in fittest_path]

    plot_tsp_path(fittest_path, coordinates_list, 'fabrica.png', path_cost)

    plot_genetic_diversity(genetic_diversity_values)


if __name__ == "__main__":
    main() #Inicia a função main quando o nome do modulo de execução for __main__

