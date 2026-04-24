import numpy as np
from app.engine.core.config import NODES

def generate_nodes(num_nodes=NODES):
    """
    Generates random geographical coordinates for IoT waste bins.

    Args:
        num_nodes (int): The total number of waste bins to simulate.

    Returns:
        numpy.ndarray: An array of shape (num_nodes, 2) containing random X and Y 
                       coordinates scaled between 0 and 100.
    """
    node_coordinates = np.random.uniform(0, 100, size=(num_nodes, 2))
    return node_coordinates

def get_depot():
    """
    Defines the central depot location for the waste collection vehicles.

    Returns:
        numpy.ndarray: An array of shape (1, 2) containing the depot's X and Y coordinates.
    """
    return np.array([[50.0, 50.0]])
