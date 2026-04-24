import matplotlib.pyplot as plt
import folium

def plot_convergence(ga_history, aco_history, hybrid_history):
    """
    Generates academic trajectory curves natively distinguishing geometric solving dynamics strictly.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(ga_history, label='GA', color='red', linewidth=2)
    plt.plot(aco_history, label='ACO', color='blue', linewidth=2)
    plt.plot(hybrid_history, label='Hybrid GA-ACO', color='green', linewidth=3)
    
    plt.xlabel('Generations / Iterations', fontsize=14, fontweight='bold')
    plt.ylabel('Total Distance', fontsize=14, fontweight='bold')
    plt.title('Convergence Comparison', fontsize=16, fontweight='bold')
    
    plt.grid(True, linestyle='--', color='lightgray', alpha=0.7)
    plt.legend(fontsize=12, loc='best')
    plt.tight_layout()
    plt.savefig('fig_convergence.png', dpi=300)
    plt.close()

def plot_cost(baseline_metric, ga_metric, aco_metric, hybrid_metric, filtered_metric):
    """
    Constructs robust column charts mapping strictly quantified terminal values tracking sequential improvements.
    """
    plt.figure(figsize=(10, 6))
    category_labels = ['Baseline', 'GA', 'ACO', 'Hybrid\n(Proposed)', 'Filtered']
    spatial_costs = [baseline_metric, ga_metric, aco_metric, hybrid_metric, filtered_metric]
    bar_colors = ['gray', 'red', 'blue', 'green', 'purple']
    
    cost_bars = plt.bar(category_labels, spatial_costs, color=bar_colors, edgecolor='black', linewidth=1, zorder=3)
    plt.ylabel('Total Distance', fontsize=14, fontweight='bold')
    plt.title('Cost Comparison', fontsize=16, fontweight='bold')
    plt.grid(True, axis='y', linestyle='--', color='lightgray', alpha=0.7, zorder=0)
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    for idx, visual_column in enumerate(cost_bars):
        if idx == 3:
            visual_column.set_edgecolor('gold')
            visual_column.set_linewidth(3.5)
            
        column_height = visual_column.get_height()
        y_offset = 0.01 * max(spatial_costs)
        plt.text(visual_column.get_x() + visual_column.get_width() / 2, column_height + y_offset, 
                 f'{column_height:.1f}', ha='center', va='bottom', fontsize=12)
        
    plt.tight_layout()
    plt.savefig('fig_cost.png', dpi=300)
    plt.close()

def plot_node_reduction(total_entities, prioritized_entities):
    """
    Contrasts base spatial entities vs dynamically filtered operational bounds mathematically.
    """
    plt.figure(figsize=(8, 6))
    comparison_labels = ['Total Nodes', 'Active Nodes']
    geometric_counts = [total_entities, prioritized_entities]
    structural_colors = ['gray', 'magenta']
    
    visual_bars = plt.bar(comparison_labels, geometric_counts, color=structural_colors, edgecolor='black', width=0.5, zorder=3)
    plt.ylabel('Number of Nodes', fontsize=14, fontweight='bold')
    plt.title('Node Reduction via Predictive Filtering', fontsize=16, fontweight='bold')
    plt.grid(True, axis='y', linestyle='--', color='lightgray', alpha=0.7, zorder=0)
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    for bar in visual_bars:
        height_value = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height_value + (0.02 * max(geometric_counts)), f'{height_value}', ha='center', va='bottom', fontsize=12)
        
    plt.tight_layout()
    plt.savefig('fig_nodes.png', dpi=300)
    plt.close()
    
def plot_computation_time(execution_times_dictionary):
    """
    Summarizes mechanical operational logic times spanning isolated component matrices internally visually.
    """
    plt.figure(figsize=(10, 6))
    metric_labels = list(execution_times_dictionary.keys())
    temporal_values = list(execution_times_dictionary.values())
    
    # Map colors systematically linearly
    temporal_colors = []
    for lbl in metric_labels:
        if lbl.upper() == 'GA': temporal_colors.append('red')
        elif lbl.upper() == 'ACO': temporal_colors.append('blue')
        elif lbl.upper() == 'HYBRID': temporal_colors.append('green')
        else: temporal_colors.append('gray')
        
    visual_bars = plt.bar(metric_labels, temporal_values, color=temporal_colors, edgecolor='black', zorder=3)
    plt.ylabel('Execution Time (seconds)', fontsize=14, fontweight='bold')
    plt.title('Computation Time Comparison', fontsize=16, fontweight='bold')
    plt.grid(True, axis='y', linestyle='--', color='lightgray', alpha=0.7, zorder=0)
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    for bar in visual_bars:
        y_max_bound = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, y_max_bound + (0.02 * max(temporal_values)), 
                 f'{y_max_bound:.2f}s', ha='center', va='bottom', fontsize=12)
        
    plt.tight_layout()
    plt.savefig('fig_time.png', dpi=300)
    plt.close()

def generate_route_map(spatial_nodes, sequenced_route):
    """
    Extracts static boundaries and structures exact visual map representations explicitly connecting contiguous points.
    """
    central_depot = spatial_nodes[0]
    
    def calculate_lat_lon(point_coords):
        mapping_latitude = 40.0 + (point_coords[0] / 100.0) * 0.5
        mapping_longitude = -74.0 + (point_coords[1] / 100.0) * 0.5
        return [mapping_latitude, mapping_longitude]
        
    interactive_map = folium.Map(location=calculate_lat_lon(central_depot), zoom_start=11)
    
    for node_id, local_point in enumerate(spatial_nodes):
        node_color = 'red' if node_id == 0 else 'blue'
        folium.CircleMarker(
            location=calculate_lat_lon(local_point),
            radius=8 if node_id == 0 else 5,
            color=node_color,
            fill=True,
            fill_color=node_color,
            popup='Depot' if node_id == 0 else f'Node {node_id}'
        ).add_to(interactive_map)
        
    tracked_polyline = [calculate_lat_lon(spatial_nodes[0])]
    for structural_index in sequenced_route:
        tracked_polyline.append(calculate_lat_lon(spatial_nodes[structural_index]))
    tracked_polyline.append(calculate_lat_lon(spatial_nodes[0]))
    
    folium.PolyLine(locations=tracked_polyline, color='green', weight=4).add_to(interactive_map)
    interactive_map.save('route_map.html')
