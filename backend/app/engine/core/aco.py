import numpy as np
import random
from distance import calculate_total_distance

def initialize_pheromones(num_nodes, initial_concentration=0.1):
    """
    Initializes a symmetric baseline pheromone matrix.

    Args:
        num_nodes (int): Total locations in the pathing environment.
        initial_concentration (float): Fixed seeding threshold strictly preventing 0.0 values.

    Returns:
        numpy.ndarray: Square matrix storing continuous pheromone variables.
    """
    return np.ones((num_nodes, num_nodes)) * initial_concentration

def construct_solution(pheromone_matrix, distance_matrix, visibility_weight_alpha=1, heuristic_beta=3):
    """
    Simulates a generic ant walking probabilities resolving an end-to-end traversal layout.

    Args:
        pheromone_matrix (numpy.ndarray): Current layout of chemical traces left by elite ants.
        distance_matrix (numpy.ndarray): Absolute spatial lookup metrics.
        visibility_weight_alpha (float): Scaling influence metric representing historical trace values.
        heuristic_beta (float): Intense scaling emphasis determining proximity biases (High = Grabbing closest nodes natively).

    Returns:
        list: Computed contiguous route path chosen stochastically iteratively.
    """
    total_locations = len(distance_matrix)
    unvisited_nodes = list(range(1, total_locations))
    current_node = 0
    generated_route = []
    
    while unvisited_nodes:
        decision_probabilities = []
        for candidate_node in unvisited_nodes:
            # ACO Probability Calculation: Numerator integrates Historical Pheromones vs Baseline Euclidean heuristics
            pheromone_trace = pheromone_matrix[current_node, candidate_node] ** visibility_weight_alpha
            visibility_heuristic = (1.0 / (distance_matrix[current_node, candidate_node] + 1e-6)) ** heuristic_beta
            decision_probabilities.append(pheromone_trace * visibility_heuristic)
            
        aggregate_sum = sum(decision_probabilities)
        if aggregate_sum == 0:
            # ACO Probability Calculation: Fallback uniform distribution logic preventing NaN lockouts natively
            decision_probabilities = [1.0/len(unvisited_nodes)] * len(unvisited_nodes)
        else:
            decision_probabilities = [probability / aggregate_sum for probability in decision_probabilities]
            
        # Select target probabilistically mapped via the explicitly calculated weighted metrics
        navigated_node = random.choices(unvisited_nodes, weights=decision_probabilities)[0]
        generated_route.append(navigated_node)
        unvisited_nodes.remove(navigated_node)
        current_node = navigated_node
        
    return generated_route

def update_pheromones(pheromone_matrix, colony_routes, colony_distances, decay_evaporation=0.1):
    """
    Decays obsolete traces and explicitly adds freshly deposited path chemicals proportionally to route quality.

    Args:
        pheromone_matrix (numpy.ndarray): Reference matrix being physically altered.
        colony_routes (list): Multi-dimensional representation of every singular iteration route constructed.
        colony_distances (list): Matching total geographic cost representing fitness bounds.
        decay_evaporation (float): Ratio natively scrubbing previous iteration data ensuring plasticity.
    """
    pheromone_matrix *= (1.0 - decay_evaporation)
    
    for iteration_route, final_distance in zip(colony_routes, colony_distances):
        if not iteration_route:
            continue
            
        path_contribution = 100.0 / final_distance
        current_location = 0
        
        for intermediate_node in iteration_route:
            pheromone_matrix[current_location, intermediate_node] += path_contribution
            pheromone_matrix[intermediate_node, current_location] += path_contribution
            current_location = intermediate_node
            
        # Loop closure adding final transit traces dynamically 
        pheromone_matrix[current_location, 0] += path_contribution
        pheromone_matrix[0, current_location] += path_contribution

def run_aco(distance_matrix, total_ants=20, max_iterations=100, visibility_weight_alpha=1.0, 
            heuristic_beta=2.0, decay_evaporation=0.5, initial_pheromone_matrix=None, 
            best_known_route=None, best_known_distance=float('inf'), elite_seeds=None):
    """
    Standard Ant Colony framework executing decentralized heuristic tracking algorithms.

    Args:
        distance_matrix (numpy.ndarray): Explicit static grid scaling distance variables.
        total_ants (int): Colony capacity per isolated generative sweep mapping.
        max_iterations (int): Loop limits configuring long range simulation runs.
        visibility_weight_alpha (float): Alpha parameter weighting historical edges.
        heuristic_beta (float): Beta scaling prioritizing contiguous close proximity hops.
        decay_evaporation (float): Configures decay mapping variables (Low = persistent historical learning).
        initial_pheromone_matrix (numpy.ndarray, optional): Supplied matrix strictly for Hybrid initialization.
        best_known_route (list, optional): Anchoring initialization route.
        best_known_distance (float, optional): Anchoring bounding limits protecting monotonic progression graphs.
        elite_seeds (list, optional): Geometric routes explicitly injected into raw ants bypassing computation uniquely.

    Returns:
        tuple: Isolated globally optimal route found, exact cost, array mapping continuous sequence iterations.
    """
    num_nodes = len(distance_matrix)
    
    if initial_pheromone_matrix is None:
        active_pheromones = initialize_pheromones(num_nodes)
    else:
        active_pheromones = initial_pheromone_matrix.copy()
        
    optimal_colony_route = best_known_route.copy() if best_known_route else None
    optimal_colony_distance = best_known_distance
    iteration_convergence_log = []
    
    extracted_seeds = elite_seeds if elite_seeds is not None else []
    
    for _ in range(max_iterations):
        iteration_routes = []
        iteration_distances = []
        
        for ant_index in range(total_ants):
            if ant_index < len(extracted_seeds):
                # Inject perfectly bounded geometrical genetic seeds explicitly cleanly
                ant_route = extracted_seeds[ant_index].copy()
            else:
                ant_route = construct_solution(active_pheromones, distance_matrix, visibility_weight_alpha, heuristic_beta)
                
            ant_route_distance = calculate_total_distance(ant_route, distance_matrix)
            
            iteration_routes.append(ant_route)
            iteration_distances.append(ant_route_distance)
            
            # Record optimization natively if bounds fall below exact minimum known costs
            if ant_route_distance < optimal_colony_distance:
                optimal_colony_distance = ant_route_distance
                optimal_colony_route = ant_route.copy()
                
        update_pheromones(active_pheromones, iteration_routes, iteration_distances, decay_evaporation)
        iteration_convergence_log.append(optimal_colony_distance)
        
    return optimal_colony_route, optimal_colony_distance, iteration_convergence_log
