import numpy as np
from sklearn.linear_model import LinearRegression
from app.engine.core.config import THRESHOLD

def simulate_fill_levels(num_nodes, days_tracked=10):
    """
    Simulates stochastic temporal variables establishing waste accumulation patterns internally mapped to bins.

    Args:
        num_nodes (int): Count of static waste entities initialized physically inside matrices.
        days_tracked (int): Span defining sequence sizes and temporal forecasting borders.

    Returns:
        numpy.ndarray: Grid block defining volumetric accumulation logic values across days.
    """
    # Array initialization mapping temporal volumes physically linearly
    fill_history_grid = np.zeros((num_nodes, days_tracked))
    
    for node_index in range(num_nodes):
        baseline_start_metric = np.random.uniform(5, 25)
        
        # Bimodal target distribution: explicit separation natively enforces 40-60% filtration threshold conditions
        if np.random.rand() < 0.5:
            forecasted_target = np.random.uniform(75, 95)
        else:
            forecasted_target = np.random.uniform(20, 60)
            
        base_accumulation_rate = (forecasted_target - baseline_start_metric) / days_tracked
        fill_history_grid[node_index, 0] = baseline_start_metric
        
        for daily_timestamp in range(1, days_tracked):
            # Formulate explicitly chaotic mechanics representing realistic urban waste structures
            periodic_fluctuation = 2.0 * np.sin(daily_timestamp * (2 * np.pi / 7.0))
            stochastic_noise_offset = np.random.normal(0, 1.5)
            
            daily_gross_addition = max(0, base_accumulation_rate + periodic_fluctuation + stochastic_noise_offset)
            fill_history_grid[node_index, daily_timestamp] = fill_history_grid[node_index, daily_timestamp-1] + daily_gross_addition
            
        # Constrain variables rigorously to explicit container bounding geometries
        fill_history_grid[node_index] = np.clip(fill_history_grid[node_index], 0, 100)
        
    return fill_history_grid

def predict_fill_levels(historical_matrix):
    """
    Extracts explicitly filtered trajectory vectors from embedded node tracking records natively scaling into LR arrays.

    Args:
        historical_matrix (numpy.ndarray): Volumetric time-series structure representing all bins locally.

    Returns:
        numpy.ndarray: Processed bounds forecasting immediately proximate daily readings uniquely.
    """
    total_nodes, days_tracked = historical_matrix.shape
    projected_forecasts = []
    
    temporal_axis = np.arange(days_tracked).reshape(-1, 1)
    
    for bin_index in range(total_nodes):
        historical_trendline = historical_matrix[bin_index]
        
        linear_projection_model = LinearRegression()
        linear_projection_model.fit(temporal_axis, historical_trendline)
        
        computed_forecast = linear_projection_model.predict([[days_tracked]])[0]
        
        # Simulate mechanical tracking variance boundaries explicitly breaking theoretically perfect data limits
        computed_forecast += np.random.normal(0, 2.5)
        projected_forecasts.append(max(0, min(100, computed_forecast)))
        
    return np.array(projected_forecasts)

def filter_active_nodes(forecast_array, dispatch_threshold_percentage=THRESHOLD):
    """
    Extracts nodal bounds flagged beyond explicit triggering capacity marks reducing total path complexity calculations.

    Args:
        forecast_array (numpy.ndarray): Sequence of projected next-day capacities evaluated logically.
        dispatch_threshold_percentage (int): Boundary delimiter mapping required dispatch boundaries.

    Returns:
        list: Filtered tracking bounds actively requiring immediate spatial tracking (shifted cleanly omitting depot).
    """
    active_targeted_indices = np.where(forecast_array >= dispatch_threshold_percentage)[0] + 1
    return active_targeted_indices.tolist()
