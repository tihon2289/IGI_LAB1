"""
Laboratory work #3 (Variant 18)
Program: Taylor series for arcsin(x), statistics, and matplotlib plot
Version: 1.0
Developer: Your Name
Date: 2026-04-27

Implements series: arcsin(x) = sum_{n=0}^{∞} ( (2n)! / (4^n (n!)^2 (2n+1) ) ) x^(2n+1), |x| ≤ 1.
Computes mean, median, mode, variance, std of partial sums.
Plots series approximation vs math.asin(x) using matplotlib.
"""

import math
import statistics
import matplotlib.pyplot as plt

class SeriesExpansion:
    """Class for computing Taylor series of arcsin(x) and related statistics."""
    def __init__(self, x, terms=10):
        if abs(x) > 1:
            raise ValueError("x must be within [-1, 1] for arcsin series")
        self.x = x
        self.terms = terms
        self.series_values = []   

    def compute_series(self):
        """
        Compute arcsin(x) using the series:
        arcsin(x) = x + x^3/6 + 3x^5/40 + ...
        General term: a_n = ((2n)! / (4^n * (n!)^2 * (2n+1))) * x^(2n+1)
        """
        self.series_values = []
        s = 0.0
        for n in range(self.terms):
            coeff = math.factorial(2*n) / ( (4**n) * (math.factorial(n)**2) * (2*n + 1) )
            term = coeff * (self.x ** (2*n + 1))
            s += term
            self.series_values.append((n, s))
        return self.series_values

    def true_value(self):
        return math.asin(self.x)

    def get_partial_sums(self):
        """Return list of partial sums (approximations)."""
        return [val for _, val in self.series_values]

    def compute_statistics(self):
        """Return dict with mean, median, mode, variance, stdev of the partial sums."""
        sums = self.get_partial_sums()
        if not sums:
            return {}
        mean = statistics.mean(sums)
        median = statistics.median(sums)
        try:
            mode = statistics.mode([round(v, 4) for v in sums])
        except statistics.StatisticsError:
            mode = "no unique mode"
        variance = statistics.variance(sums) if len(sums) > 1 else 0
        stdev = statistics.stdev(sums) if len(sums) > 1 else 0
        return {"mean": mean, "median": median, "mode": mode,
                "variance": variance, "std_dev": stdev}

    def plot_graph(self, filename="series_plot.png"):
        """Plot series approximation and true function."""
        if not self.series_values:
            self.compute_series()
        n_vals = [n for n, _ in self.series_values]
        approx_vals = [v for _, v in self.series_values]
        true_vals = [self.true_value()] * len(n_vals)

        plt.figure()
        plt.plot(n_vals, approx_vals, 'b-o', label='Series approx arcsin(x)')
        plt.plot(n_vals, true_vals, 'r--', label=f'True arcsin({self.x})')
        plt.xlabel('Number of terms n')
        plt.ylabel('f(x)')
        plt.title(f'Taylor series for arcsin({self.x})')
        plt.legend()
        plt.grid(True)
        plt.annotate(f'True value: {self.true_value():.6f}',
                     xy=(self.terms-1, self.true_value()),
                     xytext=(self.terms-3, self.true_value()*0.9),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.savefig(filename)
        plt.show()
        print(f"Plot saved as {filename}")

def run_series_demo():
    """Interactive demo for arcsin series expansion."""
    try:
        x = float(input("Enter x for arcsin(x) series (|x| <= 1): "))
        if abs(x) > 1:
            raise ValueError("x must be between -1 and 1")
        terms = int(input("Number of terms (>=1): "))
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    exp = SeriesExpansion(x, terms)
    exp.compute_series()
    stats = exp.compute_statistics()
    print("\n--- Series Expansion for arcsin({}) ---".format(x))
    for n, val in exp.series_values:
        print(f"n={n}: {val:.6f}")
    print(f"True arcsin({x}) = {exp.true_value():.6f}")
    print("\nStatistics of partial sums:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    exp.plot_graph()