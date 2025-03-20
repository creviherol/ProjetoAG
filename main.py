import re
from graph import Graph
from genetic_algorithm_tsp import GeneticAlgorithmTSP
from plot import plot_tsp_path, plot_genetic_diversity
from collections import OrderedDict


def main():
    with open('cities.txt', 'r') as file:
        cities_data = file.read()

    city_pattern = re.compile(r'(\w+):\s\((\d+),\s(\d+)\)')

    cities = city_pattern.findall(cities_data)

    if len(cities) > 94:
        raise ValueError("Cannot accept more cities.")

    city_mapping = OrderedDict((city[0], chr(i + 33)) for i, city in enumerate(cities))

    germany_graph = Graph(len(cities), False)

    for city, x, y in cities:
        germany_graph.add_node(city_mapping[city], int(x), int(y))

    germany_graph.start_city = city_mapping['A1']

    ga_tsp_germany = GeneticAlgorithmTSP(
        graph=germany_graph,
        city_names=[city for city, _, _ in cities], 
        generations=50,
        population_size=100,
        tournament_size=5,
        mutationRate=0.1,
        fitness_selection_rate=0.5,
    )

    fittest_path, path_cost = ga_tsp_germany.find_fittest_path(germany_graph)

    genetic_diversity_values = ga_tsp_germany.get_genetic_diversity_values()

    formatted_path = ' -> '.join(fittest_path)
    print('\nPath: {0}\nCost: {1}'.format(formatted_path, path_cost))

    coordinates_dict = {city: (int(x), int(y)) for city, x, y in cities}

    coordinates_list = [coordinates_dict[city] for city in fittest_path]

    plot_tsp_path(fittest_path, coordinates_list, 'fabrica.png', path_cost)

    plot_genetic_diversity(genetic_diversity_values)

if __name__ == "__main__":
    main()
