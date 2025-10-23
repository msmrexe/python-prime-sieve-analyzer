# prime_analyzer/plotter.py

"""
Handles the generation of all performance plots using Seaborn.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def generate_plots(df: pd.DataFrame, output_dir: str):
    """
    Generates and saves line plots for time and space complexity.
    
    Args:
        df: The DataFrame containing the analysis results.
        output_dir: The directory to save plot images to.
    """
    print(f"Generating plots in '{output_dir}'...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Use a clean seaborn theme
    sns.set_theme(style="whitegrid")

    # --- Plot 1: Time Complexity ---
    plt.figure(figsize=(12, 7))
    time_plot = sns.lineplot(
        data=df,
        x="n",
        y="Time (ms)",
        hue="Algorithm",
        style="Algorithm",
        markers=True,
        dashes=True
    )
    time_plot.set_title("Time Complexity Analysis (Time vs. n)", fontsize=16)
    time_plot.set_xlabel("n (Upper Bound)", fontsize=12)
    time_plot.set_ylabel("Average Time (milliseconds)", fontsize=12)
    plt.legend(title="Algorithm")
    
    filename = "time_complexity_analysis.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()
    
    # --- Plot 2: Space Complexity ---
    plt.figure(figsize=(12, 7))
    space_plot = sns.lineplot(
        data=df,
        x="n",
        y="Peak RAM (MB)",
        hue="Algorithm",
        style="Algorithm",
        markers=True,
        dashes=True
    )
    space_plot.set_title("Space Complexity Analysis (RAM vs. n)", fontsize=16)
    space_plot.set_xlabel("n (Upper Bound)", fontsize=12)
    space_plot.set_ylabel("Peak RAM Usage (Megabytes)", fontsize=12)
    plt.legend(title="Algorithm")
    
    filename = "space_complexity_analysis.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()

    print("All plots generated successfully.")
