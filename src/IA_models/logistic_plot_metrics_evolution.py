import pandas as pd
import matplotlib.pyplot as plt


def logistic_plot_metrics_evolution(metrics_values, best_metrics, output_file='metrics_evolution_plot.png'):
    """
    Plot the evolution of selected metrics over different versions.

    Parameters:
    - metrics_values (dict): A dictionary where keys are versions and values are lists of tuples (metric_name, metric_value).
    - best_metrics (list): A list of metric names to be plotted.
    - output_file (str): File name to save the resulting plot (default: 'metrics_evolution_plot.png').
    """
    # Initialize a list to store rows
    rows = []

    # Transform metrics_values into a list of dictionaries
    for version, features in metrics_values.items():
        row = {'version': version}
        for metric_name, metric_value in features:
            row[metric_name] = metric_value
        rows.append(row)

    # Convert the list of dictionaries into a DataFrame
    df_metrics = pd.DataFrame(rows)

    # Fill missing values with 0
    df_metrics = df_metrics.fillna(0)

    # Plot the metrics
    plt.figure(figsize=(10, 6))
    for metric in best_metrics:
        if metric in df_metrics:
            plt.plot(
                df_metrics['version'],
                df_metrics[metric],
                label=metric,
                marker='o'
            )

    # Add details to the plot
    plt.xlabel('Version')
    plt.ylabel('Average Importance (SHAP)')
    plt.title('Evolution of Most Important Metrics by Version')
    plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save and display the plot
    plt.savefig(output_file)
    plt.show()
