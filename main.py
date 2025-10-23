# main.py

"""
Prime Sieve Analyzer - CLI

Main entry point to run the prime sieve analysis.
This script coordinates the analysis and plotting modules.
"""

import argparse
import numpy as np
from prime_analyzer.analyzer import run_analysis
from prime_analyzer.plotter import generate_plots

def main():
    """Parses CLI arguments and runs the analysis."""
    
    parser = argparse.ArgumentParser(
        description="Run a comparative analysis of prime sieve algorithms."
    )
    parser.add_argument(
        '--max-n',
        type=int,
        default=1000000,
        help="Maximum number 'n' to find primes up to (default: 1,000,000)"
    )
    parser.add_argument(
        '--steps',
        type=int,
        default=10,
        help="Number of different 'n' values to test (default: 10)"
    )
    parser.add_argument(
        '--csv',
        type=str,
        default="sieve_results.csv",
        help="Filename to save the raw CSV data (default: sieve_results.csv)"
    )
    parser.add_argument(
        '--plots-dir',
        type=str,
        default="plots",
        help="Directory to save the output plots (default: plots)"
    )
    args = parser.parse_args()
    
    # 1. Setup the experiment parameters
    # We start from a reasonable minimum (e.g., 10,000)
    n_values = np.linspace(start=10000, stop=args.max_n, num=args.steps, dtype=int).tolist()
    
    algo_names = [
        "Sieve of Eratosthenes",
        "Sieve of Atkin",
    ]
    
    print("--- Starting Prime Sieve Analysis ---")
    print(f"Algorithms: {', '.join(algo_names)}")
    print(f"n Values: {n_values}")
    
    # 2. Run the analysis
    df = run_analysis(algo_names, n_values)
    
    # 3. Save the raw data
    df.to_csv(args.csv, index=False)
    print(f"\nRaw results saved to '{args.csv}'")
    
    # 4. Generate plots
    generate_plots(df, args.plots_dir)
    
    print("--- Analysis Complete ---")

if __name__ == "__main__":
    main()
