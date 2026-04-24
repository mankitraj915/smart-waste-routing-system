import streamlit as st
import os
import time
from datetime import datetime
import numpy as np

# Specific Module Imports
import config
from data import generate_nodes, get_depot
from distance import compute_distance_matrix, calculate_total_distance, baseline_route
from ga import run_ga
from aco import run_aco
from hybrid import run_hybrid
from prediction import simulate_fill_levels, predict_fill_levels, filter_active_nodes
from visualization import plot_convergence, plot_cost, plot_node_reduction, plot_computation_time, generate_route_map
from utils import time_it
from results import export_metrics
import streamlit.components.v1 as components

# Layout Configurations Globally
st.set_page_config(page_title="Smart Waste Routing System", layout="wide", page_icon="♻️")

st.title("Smart Waste Routing System - AI Powered Optimization")

# Sidebar parameter mappings seamlessly natively
st.sidebar.header("Simulation Settings")
num_nodes_input = st.sidebar.slider("Number of Nodes", min_value=10, max_value=100, value=config.NODES)
fill_threshold_input = st.sidebar.slider("Fill Threshold", min_value=0.5, max_value=0.9, value=config.THRESHOLD/100.0)
random_seed_input = st.sidebar.number_input("Random Seed", value=config.SEED, step=1)
run_button = st.sidebar.button("Run Simulation", type="primary")

# Persist output directory securely mapping explicitly natively
if 'sim_completed' not in st.session_state:
    st.session_state.sim_completed = False
if 'output_dir' not in st.session_state:
    st.session_state.output_dir = ""

if run_button:
    with st.spinner("Running optimization..."):
        # Anchor configurations strictly avoiding divergence
        config.apply_seeds(int(random_seed_input))
        threshold_percentage = fill_threshold_input * 100.0
        
        # Extracted timestamps logically perfectly linearly scaling
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(os.getcwd(), 'outputs', timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        # [Phase 1] Data Gen
        urban_nodes = generate_nodes(num_nodes=num_nodes_input)
        central_depot = get_depot()
        distance_matrix, total_locations_space = compute_distance_matrix(urban_nodes, central_depot)
        
        naive_route_sequence = baseline_route(len(total_locations_space))
        baseline_cost = calculate_total_distance(naive_route_sequence, distance_matrix)
        
        # [Phase 2] GA
        (ga_route, ga_cost, ga_history, _), ga_time = time_it(run_ga, distance_matrix, population_size=num_nodes_input, max_generations=100)
        
        # [Phase 3] ACO
        (aco_route, aco_cost, aco_history), aco_time = time_it(run_aco, distance_matrix, total_ants=20, max_iterations=100)
        
        # [Phase 4] Hybrid
        (hybrid_route, hybrid_cost, hybrid_history), hybrid_time = time_it(run_hybrid, distance_matrix, aco_route, aco_history)
        
        # [Phase 5] Predicting dynamically cleanly
        historical_temporal_fills = simulate_fill_levels(num_nodes=num_nodes_input, days_tracked=10)
        forecast_volume = predict_fill_levels(historical_temporal_fills)
        filtered_indices = filter_active_nodes(forecast_volume, dispatch_threshold_percentage=threshold_percentage)
        
        active_nodes_count = len(filtered_indices)
        operational_block = [0] + filtered_indices
        condensed_matrix = distance_matrix[np.ix_(operational_block, operational_block)]
        
        # [Phase 6] Re-Mapping Hybrid internally mathematically linearly scaling bounds securely explicit correctly natively smoothly
        if active_nodes_count > 2:
            (filt_aco_r, filt_aco_c, filt_aco_h), _ = time_it(run_aco, condensed_matrix, total_ants=20, max_iterations=100)
            (filt_route, filt_cost, _), filt_time = time_it(run_hybrid, condensed_matrix, filt_aco_r, filt_aco_h)
        else:
            filt_cost, filt_time, filt_route = 0.0, 0.0, []
            
        # Chart Processing strictly mapping securely inside timestamp bounds natively structurally linearly explicitly functionally cleanly natively smoothly smoothly
        original_cwd = os.getcwd()
        os.chdir(output_dir)
        try:
            plot_convergence(ga_history, aco_history, hybrid_history)
            plot_cost(baseline_cost, ga_cost, aco_cost, hybrid_cost, filt_cost)
            plot_node_reduction(num_nodes_input, active_nodes_count)
            plot_computation_time({'GA': ga_time, 'ACO': aco_time, 'Hybrid': hybrid_time, 'Filtered': filt_time})
            
            if filt_route:
                physical_route = [operational_block[i] for i in filt_route]
                generate_route_map(total_locations_space, physical_route)
        finally:
            os.chdir(original_cwd)
        
        # Mathematical Bounds precisely structurally linearly executing percentages linearly safely properly explicitly uniquely
        improve_h = ((baseline_cost - hybrid_cost) / baseline_cost) * 100 if baseline_cost > 0 else 0
        improve_f = ((hybrid_cost - filt_cost) / hybrid_cost) * 100 if hybrid_cost > 0 else 0
        
    st.success("Simulation completed successfully")
    
    st.session_state.metrics = {
        'baseline': baseline_cost,
        'ga': ga_cost,
        'aco': aco_cost,
        'hybrid': hybrid_cost,
        'filtered': filt_cost,
        'imprv_hybrid': improve_h,
        'imprv_filtered': improve_f,
        'nodes': num_nodes_input,
        'active_nodes': active_nodes_count
    }
    st.session_state.sim_completed = True
    st.session_state.output_dir = output_dir

# Result Mapping Dashboard Sections
if not st.session_state.sim_completed:
    st.info("👈 Please set your configurations in the sidebar and click 'Run Simulation' to execute the algorithm natively!")
else:
    metrics = st.session_state.metrics
    dir_path = st.session_state.output_dir
    
    st.markdown("---")
    st.markdown("## 📊 Simulation Results")
    
    # 5-Column layout cleanly organically structuring
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Baseline Distance", f"{metrics['baseline']:.2f}")
    c2.metric("GA Distance", f"{metrics['ga']:.2f}")
    c3.metric("ACO Distance", f"{metrics['aco']:.2f}")
    c4.metric("Hybrid Optimization (Proposed)", f"{metrics['hybrid']:.2f}", delta=f"{metrics['imprv_hybrid']:.2f}%", delta_color="normal")
    c5.metric("Filtered Distance", f"{metrics['filtered']:.2f}", delta=f"{metrics['imprv_filtered']:.2f}%", delta_color="normal")
    
    st.caption("💡 **Note**: Hybrid method combines ACO with local refinement for improved routing efficiency.")
    
    st.markdown("---")
    st.markdown("### 📉 Distance Reduction Summary")
    st.markdown(
        f"<h1 style='text-align: center; color: #4CAF50;'>{metrics['baseline']:.0f} ➔ {metrics['hybrid']:.0f} ➔ {metrics['filtered']:.0f}</h1>", 
        unsafe_allow_html=True
    )
    st.markdown("<p style='text-align: center; font-size: 18px;'>Progressive optimization significantly reduces total routing distance.</p>", unsafe_allow_html=True)
    
    # Calculate unified absolute bounds securely cleanly 
    absolute_reduction_percentage = ((metrics['baseline'] - metrics['filtered']) / metrics['baseline']) * 100 if metrics['baseline'] > 0 else 0
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"## 🚀 Total Distance Reduced by **{absolute_reduction_percentage:.1f}%**")
    
    st.markdown("---")
    st.markdown("## 📈 Performance Analysis")
    
    # 2x2 Grid Graphics dynamically reliably natively mapping
    g1, g2 = st.columns(2)
    path_conv = os.path.join(dir_path, 'fig_convergence.png')
    path_cost = os.path.join(dir_path, 'fig_cost.png')
    path_node = os.path.join(dir_path, 'fig_nodes.png')
    path_time = os.path.join(dir_path, 'fig_time.png')
    
    with g1:
        if os.path.exists(path_conv):
            st.image(path_conv, caption="Convergence Behavior", use_container_width=True)
        else:
            st.warning("Run simulation first")
            
        if os.path.exists(path_node):
            st.image(path_node, caption="Node Reduction via Prediction", use_container_width=True)
        else:
            st.warning("Run simulation first")
            
    with g2:
        if os.path.exists(path_cost):
            st.image(path_cost, caption="Algorithm Cost Comparison", use_container_width=True)
        else:
            st.warning("Run simulation first")
            
        if os.path.exists(path_time):
            st.image(path_time, caption="Execution Time Comparison", use_container_width=True)
        else:
            st.warning("Run simulation first")
        
    st.markdown("---")
    st.markdown("## 🗺️ Optimized Route Visualization")
    st.write("This map shows the optimized route covering only high-demand bins after predictive filtering.")
    
    map_filepath = os.path.join(dir_path, 'route_map.html')
    if os.path.exists(map_filepath):
        with open(map_filepath, 'r', encoding='utf-8') as map_f:
            html_data = map_f.read()
        
        # HTML strictly binds height dynamically wrapping width explicitly securely mapping seamlessly cleanly explicitly optimally natively  
        components.html(html_data, height=650, scrolling=True)
    else:
        st.warning("Map visualization unavailable. (Simulation requires >2 active nodes filtered organically).")
        
    st.markdown("---")
    st.markdown("## 🧠 Key Insight")
    
    dynamic_insight = (
        f"Predictive filtering reduces routing complexity, while hybrid optimization (ACO + local search) "
        f"refines routes to achieve maximum efficiency.\n\n"
        f"**Achieved ~{absolute_reduction_percentage:.0f}% reduction compared to baseline.**"
    )
    
    st.info(dynamic_insight)
