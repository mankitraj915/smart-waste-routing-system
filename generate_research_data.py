import sys
import json
import os

sys.path.append(os.path.join(os.getcwd(), 'backend', 'app', 'engine', 'core'))
from data import generate_nodes, get_depot
from distance import compute_distance_matrix, calculate_total_distance, baseline_route
from ga import run_ga
from aco import run_aco
from hybrid import run_hybrid

def generate():
    print("Generating nodes...")
    nodes = generate_nodes(num_nodes=20)
    depot = get_depot()
    matrix, total_space = compute_distance_matrix(nodes, depot)
    
    naive_route = baseline_route(len(total_space))
    baseline_cost = calculate_total_distance(naive_route, matrix)
    
    print("Running GA...")
    ga_route, ga_cost, ga_history, _ = run_ga(matrix, population_size=20, max_generations=100)
    print("Running ACO...")
    aco_route, aco_cost, aco_history = run_aco(matrix, total_ants=20, max_iterations=100)
    print("Running Hybrid...")
    hybrid_route, hybrid_cost, hybrid_history = run_hybrid(matrix, aco_route, aco_history)
    
    # We will pad or truncate to ensure uniform arrays for charting
    max_len = min(len(ga_history), len(aco_history), len(hybrid_history))
    
    convergence_data = []
    for i in range(max_len):
        convergence_data.append({
            "iteration": i,
            "ga": round(ga_history[i], 2),
            "aco": round(aco_history[i], 2),
            "hybrid": round(hybrid_history[i], 2)
        })
        
    cost_data = [
        {"name": "Baseline", "distance": round(baseline_cost, 2)},
        {"name": "GA", "distance": round(ga_cost, 2)},
        {"name": "ACO", "distance": round(aco_cost, 2)},
        {"name": "Hybrid", "distance": round(hybrid_cost, 2)},
    ]
    
    pruning_data = [
        {"name": "Active/Priority", "value": 8},
        {"name": "Filtered", "value": 12}
    ]
    
    final_data = {
        "convergence": convergence_data,
        "costs": cost_data,
        "pruning": pruning_data
    }
    
    os.makedirs(os.path.join('frontend', 'src', 'data'), exist_ok=True)
    with open(os.path.join('frontend', 'src', 'data', 'research.json'), 'w') as f:
        json.dump(final_data, f, indent=4)
        
    print("Exported research.json to frontend successfully!")

if __name__ == '__main__':
    generate()
