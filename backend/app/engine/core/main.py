import numpy as np
from data import generate_nodes, get_depot
from distance import compute_distance_matrix, calculate_total_distance, baseline_route
from ga import run_ga
from aco import run_aco
from hybrid import run_hybrid
from prediction import simulate_fill_levels, predict_fill_levels, filter_active_nodes
from visualization import plot_convergence, plot_cost, plot_node_reduction, plot_computation_time, generate_route_map
from utils import time_it
import config

def main():
    """
    Coordinates the core operational logic orchestrating end-to-end structural mappings seamlessly matching 
    publication requirements. Ensures pipeline readability explicitly.
    """
    print("\n" + "="*60)
    print(" "*14 + "SMART WASTE ROUTING SYSTEM DEMO" + " "*15)
    print("="*60)
    
    config.apply_seeds()
    
    print("\n" + "-"*60)
    print("[ PHASE 1 ] DATA GENERATION")
    print("-"*60)
    urban_nodes = generate_nodes()
    central_depot = get_depot()
    distance_matrix, total_locations_space = compute_distance_matrix(urban_nodes, central_depot)
    
    naive_route_sequence = baseline_route(len(total_locations_space))
    baseline_spatial_cost = calculate_total_distance(naive_route_sequence, distance_matrix)
    print(f">> Total Nodes         : {config.NODES}")
    print(f">> Baseline Distance   : {baseline_spatial_cost:7.2f}")
    
    print("\n" + "-"*60)
    print("[ PHASE 2 ] GA OPTIMIZATION")
    print("-"*60)
    (ga_optimal_route, ga_optimal_cost, ga_convergence_array, _), ga_temporal_metric = time_it(
        run_ga, distance_matrix, population_size=config.NODES, max_generations=100
    )
    print(f">> Best Distance       : {ga_optimal_cost:7.2f}")
    print(f">> Execution Time      : {ga_temporal_metric:7.2f}s")
    
    print("\n" + "-"*60)
    print("[ PHASE 3 ] ACO OPTIMIZATION")
    print("-"*60)
    (aco_optimal_route, aco_optimal_cost, aco_convergence_array), aco_temporal_metric = time_it(
        run_aco, distance_matrix, total_ants=20, max_iterations=100
    )
    print(f">> Best Distance       : {aco_optimal_cost:7.2f}")
    print(f">> Execution Time      : {aco_temporal_metric:7.2f}s")
    
    print("\n" + "-"*60)
    print("[ PHASE 4 ] HYBRID OPTIMIZATION")
    print("-"*60)
    (hybrid_optimal_route, hybrid_optimal_cost, hybrid_convergence_array), hybrid_temporal_metric = time_it(
        run_hybrid, distance_matrix, aco_optimal_route, aco_convergence_array
    )
    print(f">> Best Distance       : {hybrid_optimal_cost:7.2f}")
    print(f">> Execution Time      : {hybrid_temporal_metric:7.2f}s")
    
    print("\n" + "-"*60)
    print("[ PHASE 5 ] PREDICTION FILTERING")
    print("-"*60)
    historical_temporal_fills = simulate_fill_levels(num_nodes=config.NODES, days_tracked=10)
    forecasted_volume_states = predict_fill_levels(historical_temporal_fills)
    filtered_priority_indices = filter_active_nodes(forecasted_volume_states)
    print(f">> Total Nodes         : {config.NODES}")
    print(f">> Selected Nodes      : {len(filtered_priority_indices)} (>{config.THRESHOLD}% threshold)")
    
    operational_indices_block = [0] + filtered_priority_indices
    condensed_spatial_matrix = distance_matrix[np.ix_(operational_indices_block, operational_indices_block)]
    
    (filtered_route_schema, filtered_schema_cost, _), filtered_temporal_metric = time_it(
        run_hybrid, condensed_spatial_matrix
    )
    print(f">> Filtered Distance   : {filtered_schema_cost:7.2f}")
    print(f">> Filtered Exec Time  : {filtered_temporal_metric:7.2f}s")
    
    print("\n" + "-"*60)
    print("[ PHASE 6 ] VISUALIZATION")
    print("-"*60)
    plot_convergence(ga_convergence_array, aco_convergence_array, hybrid_convergence_array)
    plot_cost(baseline_spatial_cost, ga_optimal_cost, aco_optimal_cost, hybrid_optimal_cost, filtered_schema_cost)
    plot_node_reduction(config.NODES, len(filtered_priority_indices))
    plot_computation_time({
        'GA': ga_temporal_metric, 
        'ACO': aco_temporal_metric, 
        'Hybrid': hybrid_temporal_metric,
        'Filtered Extraction': filtered_temporal_metric
    })
    
    physical_geographic_route = [operational_indices_block[filtered_pointer] for filtered_pointer in filtered_route_schema]
    generate_route_map(total_locations_space, physical_geographic_route)
    
    print(">> Graphs Generated    : fig_convergence, fig_cost, fig_nodes, fig_time")
    print(">> Maps Generated      : route_map.html")
    print("\n" + "="*60)
    print(" "*18 + "DEMO EXECUTION COMPLETE" + " "*19)
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
