# Prime Sieve Analyzer

This project is a Python tool for the empirical analysis of prime-finding algorithms, implemented for an Algorithms & Data Structures Course. It compares the practical performance (execution time and memory usage) of two key algorithms:

1.  **Sieve of Eratosthenes:** The classic, simple, and widely-known algorithm.
2.  **Sieve of Atkin:** A more modern, theoretically faster, but more complex algorithm.

The tool runs both algorithms across a range of upper bounds ($n$), measures their performance, saves the raw data to a `.csv` file, and generates a set of comparison plots. This allows for a direct comparison between the theoretical, mathematical complexity and the real-world, practical performance.

## Features

* **Algorithm Comparison:** Empirically tests the Sieve of Eratosthenes against the Sieve of Atkin.
* **Dual Analysis:** Measures both **Time Complexity** (using `timeit`) and **Space Complexity** (using `tracemalloc`).
* **Automatic Plotting:** Uses `seaborn` and `matplotlib` to generate clean comparison plots for Time vs. $n$ and RAM vs. $n$.
* **Data Export:** Saves all raw results to a `.csv` file for further analysis.
* **Modular Package:** All logic is cleanly structured in a `prime_analyzer` package.

## Project Structure

```
python-prime-sieve-analyzer/
├── .gitignore
├── LICENSE
├── README.md                # This documentation
├── requirements.txt         # Project dependencies
├── main.py                  # Main runnable script (CLI)
└── prime_analyzer/
    ├── __init__.py          # Makes 'prime_analyzer' a package
    ├── sieves.py            # Implementations of SoE and SoA
    ├── analyzer.py          # The time/space analysis runner
    └── plotter.py           # Plot generation logic
```

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/msmrexe/python-prime-sieve-analyzer.git
    cd python-prime-sieve-analyzer
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the analysis:**
    ```bash
    # Run with default settings (max_n = 1,000,000, 10 steps)
    python main.py
    
    # Run a larger, more detailed analysis
    python main.py --max-n 5000000 --steps 20
    
    # Specify output files
    python main.py --csv my_data.csv --plots-dir my_plots
    ```
    After running, check the `plots/` directory for your `.png` graphs and `sieve_results.csv` for the raw data.

---

## How the Sieves Work

### The Sieve of Eratosthenes (SoE)

This algorithm finds primes using a "process of elimination" approach.

1.  Create a list of boolean flags, `prime[0...n]`, and initialize all entries to `True`.
2.  Mark `prime[0]` and `prime[1]` as `False`.
3.  Start with the first prime number, $p = 2$.
4.  While $p^2 \le n$:
    * If `prime[p]` is `True`, then $p$ is a prime.
    * Mark all multiples of $p$ from $p^2$ to $n$ as `False` (i.e., `prime[p^2]`, `prime[p^2+p]`, `prime[p^2+2p]`, ...).
    * Find the next number $p$ greater than the current $p$ that is still marked `True`.
5.  After the loop finishes, iterate through the `prime` array. All indices $p$ for which `prime[p]` is `True` are prime numbers.

### The Sieve of Atkin (SoA)

This is a more complex, modern optimization. It performs a similar "elimination" but is more efficient by avoiding redundant operations.

1.  Create a results list, `sieve[0...n]`, and initialize all entries to `False`.
2.  Add 2 and 3 to the list of primes.
3.  The algorithm is based on quadratic forms. It iterates through all numbers $(x, y)$ up to $\sqrt{n}$.
    * For each $(x, y)$, it calculates three numbers:
        * $a = (4x^2) + (y^2)$
        * $b = (3x^2) + (y^2)$
        * $c = (3x^2) - (y^2)$ (for $x > y$)
    * It *flips the boolean value* (e.g., `sieve[num] = not sieve[num]`) for each of these numbers that falls within a specific congruence class modulo 12:
        * $a$ is flipped if it has a remainder of 1 or 5 when divided by 12.
        * $b$ is flipped if it has a remainder of 7.
        * $c$ is flipped if it has a remainder of 11.
4.  This "flipping" process correctly identifies "prime candidates."
5.  Finally, it iterates from $r = 5$ to $\sqrt{n}$. If `sieve[r]` is `True`, it marks all multiples of $r^2$ (e.g., $r^2, 2r^2, 3r^2, \dots$) as `False`. This final step eliminates any composite numbers that masqueraded as primes.
6.  The final list of primes is all $p$ for which `sieve[p]` is `True`.

---

## Theoretical Performance Analysis

### Time Complexity

* **Sieve of Eratosthenes:** The runtime is **$O(n \log \log n)$**.
    This is derived from the total number of "crossing off" operations. The algorithm sums $n/p$ for all primes $p \le n$. This sum is related to the Prime Harmonic Series, which is known to grow as $\log(\log(n))$. Therefore, the total time is $n \times (\log \log n)$.

* **Sieve of Atkin:** The runtime is **$O(n / \log \log n)$**.
    This is asymptotically *faster* than Eratosthenes. It achieves this by using the quadratic forms to perform fewer operations overall, avoiding the redundant "crossing off" for composite numbers that Eratosthenes performs.

### Space Complexity

* **Both Algorithms:** The space complexity for both is **$O(n)$**.
    Both algorithms are dominated by the need to create a boolean "sieve" array of size $n+1$ to store the prime/composite status of every number from 0 to $n$.

---

## Empirical Performance Analysis

This is what the generated plots show.

### Time vs. $n$ (Time Complexity Plot)

This plot reveals a key difference between theory and practice.

* The runtimes for both algorithms appear to grow in a **near-linear** fashion. The $O(n \log \log n)$ and $O(n / \log \log n)$ terms are very close to $O(n)$ in practice, as $\log \log n$ grows incredibly slowly.
* **The Sieve of Eratosthenes (SoE) is visibly faster** than the Sieve of Atkin (SoA) across the tested range (e.g., up to $n = 5,000,000$).
* **Reason:** The Sieve of Atkin has a *much higher constant overhead*. Its setup and the complex quadratic loops are computationally expensive. The asymptotic advantage of SoA only begins to appear at *extremely* large values of $n$, far beyond what is typically analyzed in this type of experiment.

### Peak RAM vs. $n$ (Space Complexity Plot)

This plot provides a perfect confirmation of the theoretical analysis.

* We see **two almost perfectly straight lines**, starting near zero and increasing linearly.
* This empirically validates the **$O(n)$ space complexity** for both algorithms. The plots will clearly show that doubling the input $n$ also doubles the memory required, just as the theory predicts.

## Conclusion

* For **practical use**, the **Sieve of Eratosthenes is the recommended algorithm** for finding all primes up to $n$ (for $n$ up to $\approx 10^8$ or $10^9$). Its simplicity and low constant overhead make it significantly faster than the Sieve of Atkin in real-world scenarios.
* The primary **limitation** of both sieves is their **$O(n)$ space complexity**, which makes them unusable for finding primes up to very large numbers (e.g., $n = 10^{12}$) on standard hardware.
* To solve this memory problem, **segmented sieves** are used, which apply the logic of Eratosthenes in $O(\sqrt{n})$ memory-sized blocks.

---

## Author

Feel free to connect or reach out if you have any questions!

* **Maryam Rezaee**
* **GitHub:** [@msmrexe](https://github.com/msmrexe)
* **Email:** [ms.maryamrezaee@gmail.com](mailto:ms.maryamrezaee@gmail.com)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
