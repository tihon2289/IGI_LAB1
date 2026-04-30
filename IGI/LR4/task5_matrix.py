"""
Laboratory work #5 (Variant 18)
Program: NumPy matrix operations and statistics
Version: 1.0
Developer: Your Name
Date: 2026-04-27

Task: Find column with minimal sum of elements.
Compute median of that column (two ways: np.median and manual).
Matrix generated randomly.
"""

import numpy as np

class MatrixAnalyzer:
    """Handles matrix generation, analysis and statistics."""
    def __init__(self, n=5, m=5):
        self.n = n
        self.m = m
        self.matrix = np.random.randint(1, 20, size=(n, m))

    def min_sum_column_index(self):
        """Return index of column with smallest sum."""
        col_sums = self.matrix.sum(axis=0)
        return np.argmin(col_sums)

    def column_median_builtin(self, col_idx):
        """Median using numpy."""
        return np.median(self.matrix[:, col_idx])

    def column_median_manual(self, col_idx):
        """Calculate median manually (sorted, middle)."""
        col = sorted(self.matrix[:, col_idx])
        length = len(col)
        if length % 2 == 1:
            return col[length // 2]
        else:
            return (col[length // 2 - 1] + col[length // 2]) / 2.0

    def row_sums(self):
        return self.matrix.sum(axis=1)

    def min_row_sum(self):
        return np.min(self.row_sums())

    def mean_all(self):
        return np.mean(self.matrix)

    def median_all(self):
        return np.median(self.matrix)

    def corrcoef_example(self):
        """Correlation coefficient between even and odd index elements (flattened)."""
        flat = self.matrix.flatten()
        even_indices = flat[::2]
        odd_indices = flat[1::2]
        if len(even_indices) != len(odd_indices):
            min_len = min(len(even_indices), len(odd_indices))
            even_indices = even_indices[:min_len]
            odd_indices = odd_indices[:min_len]
        if len(even_indices) < 2:
            return 0
        corr_matrix = np.corrcoef(even_indices, odd_indices)
        return corr_matrix[0, 1]

    def variance_all(self):
        return np.var(self.matrix)

    def std_all(self):
        return np.std(self.matrix)

def run_matrix_demo():
    """Interactive matrix analysis."""
    try:
        n = int(input("Number of rows: "))
        m = int(input("Number of columns: "))
    except ValueError:
        print("Invalid input, using 5x5.")
        n, m = 5, 5

    analyzer = MatrixAnalyzer(n, m)
    print("Generated matrix:")
    print(analyzer.matrix)

    col_idx = analyzer.min_sum_column_index()
    print(f"\nColumn with minimum sum: index {col_idx} (0-based)")

    median_b = analyzer.column_median_builtin(col_idx)
    median_m = analyzer.column_median_manual(col_idx)
    print(f"Median (built-in): {median_b}")
    print(f"Median (manual): {median_m}")

    corr = analyzer.corrcoef_example()
    print(f"Correlation coefficient (even vs odd indices): {corr:.4f}")

    print(f"\nMean of whole matrix: {analyzer.mean_all():.2f}")
    print(f"Variance: {analyzer.variance_all():.2f}")
    print(f"Standard deviation: {analyzer.std_all():.2f}")