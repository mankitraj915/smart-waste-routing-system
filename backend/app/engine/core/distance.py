import numpy as np

def compute_distance_matrix(nodes, depot):
    """
    Computes a symmetric Euclidean distance matrix between all geographical points.

    Args:
        nodes (numpy.ndarray): Geographical coordinates of all waste nodes.
        depot (numpy.ndarray): Geographical coordinate of the vehicle depot.

    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: A 2D symmetric array representing distances between every pair of points.
            - numpy.ndarray: An array containing the depot at index 0 followed by all nodes.
    """
    all_points = np.vstack([depot, nodes])
    total_locations = len(all_points)
    distance_matrix = np.zeros((total_locations, total_locations))
    
    for i in range(total_locations):
        for j in range(total_locations):
            distance_matrix[i, j] = np.linalg.norm(all_points[i] - all_points[j])
            
    return distance_matrix, all_points

def calculate_total_distance(route, distance_matrix):
    """
    Calculates the total travel distance of a given route sequence, including 
    departure from and return to the depot.

    Args:
        route (list of int): Ordered list of node indices to visit natively (excluding depot).
        distance_matrix (numpy.ndarray): The precomputed Euclidean distance matrix.

    Returns:
        float: The cumulative calculated distance of the entire route.
    """
    if not route:
        return 0.0
        
    total_distance = 0.0
    current_location = 0  # Vehicles always start at the depot (index 0)
    
    for next_location in route:
        total_distance += distance_matrix[current_location, next_location]
        current_location = next_location
        
    # Append the final return trip back up to the central depot
    total_distance += distance_matrix[current_location, 0]
    return total_distance

def baseline_route(total_locations):
    """
    Generates a naive, baseline sequence connecting nodes strictly sequentially.

    Args:
        total_locations (int): The overall count of nodes including the depot.

    Returns:
        list of int: A simplistic sequential route [1, 2, 3, ... N-1].
    """
    return list(range(1, total_locations))
