import argparse
import os
import time
from datetime import datetime
import numpy as np

from data import generate_nodes, get_depot
from distance import compute_distance_matrix, calculate_total_distance, baseline_route
from ga import run_ga
from aco import run_aco
from hybrid import run_hybrid
from prediction import simulate_fill_levels, predict_fill_levels, filter_active_nodes
from visualization import plot_convergence, plot_cost, plot_node_reduction, plot_computation_time, generate_route_map
from utils import time_it
from results import export_metrics
import config

def main():
    parser = argparse.ArgumentParser(description="End-to-End Smart Waste Routing System Demo")
    parser.add_argument('--nodes', type=int, default=config.NODES, help=f'Total number of nodes (default: {config.NODES})')
    parser.add_argument('--seed', type=int, default=config.SEED, help=f'Random seed for reproducibility (default: {config.SEED})')
    parser.add_argument('--threshold', type=float, default=config.THRESHOLD, help=f'Prediction filtering threshold percent (default: {config.THRESHOLD})')
    
    args = parser.parse_args()
    
    # Set localized environmental seed mapping centrally
    config.apply_seeds(args.seed)
    
    # Extract Output Directory mathematically resolving cleanly structurally
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.getcwd(), 'outputs', timestamp)
    os.makedirs(output_dir, exist_ok=True)
    
    # Base execution
    print("\n" + "="*60)
    print(" "*14 + "SMART WASTE ROUTING SYSTEM DEMO" + " "*15)
    print("="*60)
    
    # Phase 1: Data
    urban_nodes = generate_nodes(num_nodes=args.nodes)
    central_depot = get_depot()
    distance_matrix, total_locations_space = compute_distance_matrix(urban_nodes, central_depot)
    
    naive_route_sequence = baseline_route(len(total_locations_space))
    baseline_spatial_cost = calculate_total_distance(naive_route_sequence, distance_matrix)
    print(f"[Phase 1] Data Gen | Nodes: {args.nodes} | Baseline Distance: {baseline_spatial_cost:.2f}")
    
    # Phase 2: GA
    (ga_optimal_route, ga_optimal_cost, ga_convergence_array, _), ga_temporal_metric = time_it(
        run_ga, distance_matrix, population_size=args.nodes, max_generations=100
    )
    print(f"[Phase 2] GA       | Expected Distance: {ga_optimal_cost:.2f} | Execution: {ga_temporal_metric:.2f}s")
    
    # Phase 3: ACO
    (aco_optimal_route, aco_optimal_cost, aco_convergence_array), aco_temporal_metric = time_it(
        run_aco, distance_matrix, total_ants=20, max_iterations=100
    )
    print(f"[Phase 3] ACO      | Expected Distance: {aco_optimal_cost:.2f} | Execution: {aco_temporal_metric:.2f}s")
    
    # Phase 4: Hybrid
    (hybrid_optimal_route, hybrid_optimal_cost, hybrid_convergence_array), hybrid_temporal_metric = time_it(
        run_hybrid, distance_matrix, aco_optimal_route, aco_convergence_array
    )
    print(f"[Phase 4] Hybrid   | Expected Distance: {hybrid_optimal_cost:.2f} | Execution: {hybrid_temporal_metric:.2f}s")
    
    # Phase 5: Filter
    historical_temporal_fills = simulate_fill_levels(num_nodes=args.nodes, days_tracked=10)
    forecasted_volume_states = predict_fill_levels(historical_temporal_fills)
    filtered_priority_indices = filter_active_nodes(forecasted_volume_states, dispatch_threshold_percentage=args.threshold)
    print(f"[Phase 5] Filter   | Active Nodes: {len(filtered_priority_indices)} (>{args.threshold}%)")
    
    operational_indices_block = [0] + filtered_priority_indices
    condensed_spatial_matrix = distance_matrix[np.ix_(operational_indices_block, operational_indices_block)]
    
    # Phase 6: Filtered Hybrid
    if len(filtered_priority_indices) > 2:
        (filt_aco_route, filt_aco_cost, filt_aco_hist), _ = time_it(run_aco, condensed_spatial_matrix, total_ants=20, max_iterations=100)
        (filtered_route_schema, filtered_schema_cost, _), filtered_temporal_metric = time_it(
            run_hybrid, condensed_spatial_matrix, filt_aco_route, filt_aco_hist
        )
    else:
        filtered_schema_cost = 0.0
        filtered_temporal_metric = 0.0
        filtered_route_schema = []
        
    print(f"[Phase 6] Re-Hybrid| Filtered Distance: {filtered_schema_cost:.2f} | Execution: {filtered_temporal_metric:.2f}s")
    
    # Change DIR securely mathematically preserving logic internally 
    original_cwd = os.getcwd()
    os.chdir(output_dir)
    try:
        plot_convergence(ga_convergence_array, aco_convergence_array, hybrid_convergence_array)
        plot_cost(baseline_spatial_cost, ga_optimal_cost, aco_optimal_cost, hybrid_optimal_cost, filtered_schema_cost)
        plot_node_reduction(args.nodes, len(filtered_priority_indices))
        plot_computation_time({
            'GA': ga_temporal_metric, 
            'ACO': aco_temporal_metric, 
            'Hybrid': hybrid_temporal_metric,
            'Filtered': filtered_temporal_metric
        })
        
        if filtered_route_schema:
            physical_geographic_route = [operational_indices_block[filtered_pointer] for filtered_pointer in filtered_route_schema]
            generate_route_map(total_locations_space, physical_geographic_route)
    finally:
        os.chdir(original_cwd)
        
    print(f"\n>> All Visual outputs safely compiled locally internally: {output_dir}")
    
    # SUMMARY Mathematical Formatting explicitly generated linearly 
    print("\n" + "="*60)
    print(" "*25 + "SUMMARY" + " "*25)
    print("="*60)
    print(f"Baseline        : {baseline_spatial_cost:7.2f}")
    print(f"GA              : {ga_optimal_cost:7.2f}")
    print(f"ACO             : {aco_optimal_cost:7.2f}")
    print(f"Hybrid          : {hybrid_optimal_cost:7.2f}")
    print(f"Filtered Hybrid : {filtered_schema_cost:7.2f} (Active Nodes: {len(filtered_priority_indices)})")
    
    # Math strictly bounds percentage outputs linearly effectively securely
    improvement_to_hybrid = ((baseline_spatial_cost - hybrid_optimal_cost) / baseline_spatial_cost) * 100
    
    improvement_to_filtered = 0.0
    if hybrid_optimal_cost > 0:
        improvement_to_filtered = ((hybrid_optimal_cost - filtered_schema_cost) / hybrid_optimal_cost) * 100
    
    print("\n[ Performance Metrics ]")
    print(f">> Baseline to Hybrid Improvement  : {improvement_to_hybrid:.2f}%")
    print(f">> Hybrid to Filtered Improvement  : {improvement_to_filtered:.2f}%")
    
    metrics_compilation = {
        'Distances': {
            'Baseline': baseline_spatial_cost,
            'GA': ga_optimal_cost,
            'ACO': aco_optimal_cost,
            'Hybrid': hybrid_optimal_cost,
            'Filtered Hybrid': filtered_schema_cost
        },
        'Execution Times': {
            'GA': ga_temporal_metric,
            'ACO': aco_temporal_metric,
            'Hybrid': hybrid_temporal_metric,
            'Filtered Hybrid': filtered_temporal_metric
        },
        'Node Counts': {
            'Total Nodes': args.nodes,
            'Active Nodes': len(filtered_priority_indices)
        },
        'Improvements (%)': {
            'Baseline to Hybrid': improvement_to_hybrid,
            'Hybrid to Filtered': improvement_to_filtered
        }
    }
    
    export_metrics(metrics_compilation, output_dir)
    print(">> Results successfully exported logically linearly format [results.json, results.csv]")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
