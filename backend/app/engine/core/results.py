import json
import csv
import os

def export_metrics(metrics_dictionary, output_directory):
    """
    Persists structured algorithmic evaluation boundaries onto permanent disk formats cleanly systematically.

    Args:
        metrics_dictionary (dict): Aggregated structured numericals mapped across exact computational variables linearly.
        output_directory (str): Explicit path target strictly dumping generated metrics natively bypassing global tracks.
    """
    json_path = os.path.join(output_directory, 'results.json')
    csv_path = os.path.join(output_directory, 'results.csv')
    
    # Dump hierarchical structures mathematically cleanly
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(metrics_dictionary, json_file, indent=4)
        
    # Flatten dynamically and persist raw columns securely mapping relational arrays securely
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Category', 'Metric', 'Value'])
        
        for primary_category, sub_metrics in metrics_dictionary.items():
            if isinstance(sub_metrics, dict):
                for specific_metric, explicit_value in sub_metrics.items():
                    # Format decimals linearly cleanly natively extracting numeric constraints
                    formatted_val = f"{explicit_value:.4f}" if isinstance(explicit_value, float) else explicit_value
                    csv_writer.writerow([primary_category, specific_metric, formatted_val])
            else:
                formatted_val = f"{sub_metrics:.4f}" if isinstance(sub_metrics, float) else sub_metrics
                csv_writer.writerow(['General', primary_category, formatted_val])
