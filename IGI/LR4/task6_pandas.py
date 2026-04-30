"""
Laboratory work #6 (Variant 18)
Program: Pandas – Loan Prediction dataset exploration
Version: 1.0
Developer: Your Name
Date: 2026-04-27

Part A: Create DataFrame from dict with custom indices.
Part B: Statistical analysis – ratio of incomes between max/min loan amounts.
"""

import pandas as pd
import numpy as np

class LoanAnalysis:
    """Encapsulates loan data analysis."""
    def __init__(self, data_dict=None):
        if data_dict is None:
            data_dict = {
                'ApplicantIncome': [5000, 6000, 8000, 3000],
                'LoanAmount': [150, 200, 250, 120]
            }
        self.df = pd.DataFrame(data_dict)
        if list(self.df.index) == list(range(len(self.df))):
            self.df.index = [f'borrower{i+1}' for i in range(len(self.df))]

    def display_data(self):
        print("DataFrame:")
        print(self.df)

    def create_series_example(self):
        """Demonstrate Series creation and operations."""
        incomes = pd.Series(self.df['ApplicantIncome'].values,
                            index=self.df.index, name='Income')
        print("Series from ApplicantIncome:")
        print(incomes)

    def ratio_incomes_maxmin_loan(self):
        """
        Task B: Ratio of average income for max LoanAmount vs min LoanAmount.
        Returns tuple (ratio, avg_max_income, avg_min_income).
        """
        max_loan = self.df['LoanAmount'].max()
        min_loan = self.df['LoanAmount'].min()
        max_income_avg = self.df[self.df['LoanAmount'] == max_loan]['ApplicantIncome'].mean()
        min_income_avg = self.df[self.df['LoanAmount'] == min_loan]['ApplicantIncome'].mean()
        if min_income_avg == 0:
            return np.inf
        ratio = max_income_avg / min_income_avg
        return ratio, max_income_avg, min_income_avg

    def additional_stats(self):
        """Print additional statistics."""
        print("\nBasic statistics:")
        print(self.df.describe())

def run_pandas_demo():
    """Interactive pandas demo for variant 18."""
    data_dict = {
        'ApplicantIncome': [5000, 6000, 8000, 3000],
        'LoanAmount': [150, 200, 250, 120]
    }
    loan = LoanAnalysis(data_dict)
    print("=== Part A: DataFrame creation ===")
    loan.display_data()
    loan.create_series_example()

    ratio, avg_max, avg_min = loan.ratio_incomes_maxmin_loan()
    print(f"\n=== Part B: Ratio Analysis ===")
    print(f"Average income for max loan ({loan.df['LoanAmount'].max()}): {avg_max:.2f}")
    print(f"Average income for min loan ({loan.df['LoanAmount'].min()}): {avg_min:.2f}")
    print(f"Ratio (max/min): {ratio:.2f}")

    loan.additional_stats()