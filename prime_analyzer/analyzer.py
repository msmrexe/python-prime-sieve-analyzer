# prime_analyzer/analyzer.py

"""
Handles the empirical analysis of sieve algorithms.

Runs time (timeit) and space (tracemalloc) analysis
for different algorithms and 'n' values.
"""

import timeit
import tracemalloc
import pandas as pd
from .sieves import ALGORITHM_MAP

def run_analysis(algo_names: list[str], n_values: list[int]) -> pd.DataFrame:
    """
    Runs time and space analysis for given algorithms and n-values.
    
    Args:
        algo_names: List of algorithm names to test (from ALGORITHM_MAP).
        n_values: List of integers 'n' to test up to.
        
    Returns:
        A pandas DataFrame with the results.
    """
    results = []
    
    for n in n_values:
        print(f"Analyzing for n = {n}...")
        for name in algo_names:
            if name not in ALGORITHM_MAP:
                print(f"Warning: Algorithm '{name}' not found. Skipping.")
                continue
            
            func = ALGORITHM_MAP[name]
            
            # --- Time Analysis ---
            # We use a lambda to pass 'n' to the function
            # We run it 5 times and take the average
            num_runs = 5
            try:
                timer = timeit.timeit(lambda: func(n), number=num_runs)
                time_avg_ms = (timer / num_runs) * 1000  # Average time in milliseconds
            except Exception as e:
                print(f"Error timing {name} at n={n}: {e}")
                time_avg_ms = None

            # --- Space Analysis ---
            try:
                tracemalloc.start()
                func(n) # Run the function
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                peak_mb = peak / (1024 * 1024) # Peak memory in Megabytes
            except Exception as e:
                print(f"Error profiling memory for {name} at n={n}: {e}")
                peak_mb = None

            # Append results
            results.append({
                "Algorithm": name,
                "n": n,
                "Time (ms)": time_avg_ms,
                "Peak RAM (MB)": peak_mb,
            })
            
    return pd.DataFrame(results)
