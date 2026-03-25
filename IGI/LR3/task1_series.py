"""
Purpose: Task 1 - Taylor series calculation (Variant 12).
Note: Since the specific function wasn't provided in the prompt, e^x is used.
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""
import math

def calculate_taylor_series(x: float, eps: float, max_iter: int = 500) -> tuple:
    """
    Calculates the Taylor series for e^x.
    
    :param x: Argument value.
    :param eps: Precision.
    :param max_iter: Maximum iterations limit.
    :return: Tuple of (calculated_value, number_of_terms)
    """
    n = 0
    term = 1.0
    series_sum = 0.0
    
    while abs(term) >= eps and n < max_iter:
        series_sum += term
        n += 1
        term = (x ** n) / math.factorial(n)
        
    return series_sum, n

def print_series_result(x: float, eps: float):
    """Business logic for task 1: formats and prints the result."""
    try:
        f_x, n = calculate_taylor_series(x, eps)
        math_fx = math.exp(x)
        
        print(f"{'x':<10} | {'F(x)':<20} | {'n':<5} | {'Math F(x)':<20}")
        print("-" * 65)
        print(f"{x:<10} | {f_x:<20.8f} | {n:<5} | {math_fx:<20.8f}")
    except OverflowError:
        print("Error: The result is too large to be calculated (Overflow).")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")