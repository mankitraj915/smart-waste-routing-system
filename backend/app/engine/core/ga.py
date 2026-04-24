import numpy as np
import random
from distance import calculate_total_distance

def initialize_population(population_size, num_nodes):
    """
    Generates an initial randomized population of route permutations.
    
    Args:
        population_size (int): The number of individual routes in a generation.
        num_nodes (int): The total number of nodes (including depot).
        
    Returns:
        list of lists: A collection of distinct randomized traveling routes.
    """
    population_pool = []
    base_sequence = list(range(1, num_nodes))
    for _ in range(population_size):
        randomized_route = base_sequence.copy()
        random.shuffle(randomized_route)
        population_pool.append(randomized_route)
    return population_pool

def fitness_function(route, distance_matrix):
    """
    Evaluates the quality of a route inversion (fitness = 1 / distance).
    
    Args:
        route (list): The sequence of nodes.
        distance_matrix (numpy.ndarray): The lookup table for node distances.
        
    Returns:
        float: The normalized geometric fitness score.
    """
    return 1.0 / (calculate_total_distance(route, distance_matrix) + 1e-6)

def tournament_selection(population_pool, fitness_scores, tournament_size=5):
    """
    Conducts tournament selection to isolate optimal parents for mating.
    
    Args:
        population_pool (list): The current population routes.
        fitness_scores (list): The parallel list matching population fitness mappings.
        tournament_size (int): Pressure metric regulating selection intensity.
        
    Returns:
        list: The single route sub-chromosome algorithmically selected to mate.
    """
    contender_indices = random.sample(range(len(population_pool)), min(tournament_size, len(population_pool)))
    champion_index = max(contender_indices, key=lambda idx: fitness_scores[idx])
    return population_pool[champion_index]

def ordered_crossover(parent_one, parent_two):
    """
    Executes ordered order crossover (OX) to generate a valid child permutation.
    
    Args:
        parent_one (list): The primary donor route algorithmically matched.
        parent_two (list): The secondary trait contributor route.
        
    Returns:
        list: Offspring permutation avoiding cyclic nodal duplications.
    """
    genome_size = len(parent_one)
    if genome_size < 2:
        return parent_one.copy()
        
    # GA Operation: Determine splicing block coordinates
    slice_start, slice_end = sorted(random.sample(range(genome_size), 2))
    offspring = [-1] * genome_size
    
    # GA Operation: Inherit primary genetic segment cleanly
    offspring[slice_start:slice_end] = parent_one[slice_start:slice_end]
    
    # GA Operation: Cascade remaining alleles safely omitting duplicate traits
    parent_two_pointer = 0
    for i in range(genome_size):
        if offspring[i] == -1:
            while parent_two[parent_two_pointer] in offspring:
                parent_two_pointer += 1
            offspring[i] = parent_two[parent_two_pointer]
            
    return offspring

def swap_mutation(route, mutation_probability=0.05):
    """
    Applies small mutation noise by explicitly randomly exchanging two path nodes.
    
    Args:
        route (list): Individual permutation targeted for mutation.
        mutation_probability (float): Baseline threshold metric limiting volatility.
        
    Returns:
        list: The internally spliced route (possibly unchanged).
    """
    if len(route) < 2:
        return route
        
    # GA Operation: Evaluate explicit disruption bounds via probability parameter
    if random.random() < mutation_probability:
        index_a, index_b = random.sample(range(len(route)), 2)
        route[index_a], route[index_b] = route[index_b], route[index_a]
    return route

def run_ga(distance_matrix, population_size=50, max_generations=100):
    """
    Executes a structured Genetic Algorithm configured for early convergence tracking.
    
    Args:
        distance_matrix (numpy.ndarray): Euclidean grid scaling nodes.
        population_size (int): Constraints on active entities simultaneously alive.
        max_generations (int): Loop limits before termination sequences run.
        
    Returns:
        tuple: Represents (Optimal computed route layout, final aggregate distance, 
               generational historical arrays mapping optimization progression, top elites block).
    """
    num_nodes = len(distance_matrix)
    population_pool = initialize_population(population_size, num_nodes)
    
    global_best_route = None
    global_best_distance = float('inf')
    convergence_history = []
    final_elites = []
    
    for generation in range(max_generations):
        # Calculate survival probabilities derived from path efficiency
        fitness_scores = [fitness_function(ind, distance_matrix) for ind in population_pool]
        
        champion_index = np.argmax(fitness_scores)
        generation_champion = population_pool[champion_index]
        generation_distance = calculate_total_distance(generation_champion, distance_matrix)
        
        # Globally log new absolute solutions preventing historical fade
        if generation_distance < global_best_distance:
            global_best_distance = generation_distance
            global_best_route = generation_champion.copy()
            
        convergence_history.append(global_best_distance)
        
        # GA Operation: High elitism parameters physically cause aggressive local plateauing
        sorted_ranking_indices = np.argsort(fitness_scores)[::-1]
        elite_pool_size = max(1, int(0.2 * population_size))
        elite_subgroup = [population_pool[idx] for idx in sorted_ranking_indices[:elite_pool_size]]
        
        if generation == max_generations - 1:
            final_elites = elite_subgroup
            
        new_population_pool = [elite.copy() for elite in elite_subgroup]
        
        # Populate missing voids via explicit breeding mappings
        while len(new_population_pool) < population_size:
            father_entity = tournament_selection(population_pool, fitness_scores)
            mother_entity = tournament_selection(population_pool, fitness_scores)
            infant_entity = ordered_crossover(father_entity, mother_entity)
            infant_entity = swap_mutation(infant_entity)
            new_population_pool.append(infant_entity)
            
        population_pool = new_population_pool
        
    return global_best_route, global_best_distance, convergence_history, final_elites
