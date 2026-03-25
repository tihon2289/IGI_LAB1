"""
Purpose: Utility functions for input validation and decorators.
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""

def ui_separator(char='-', length=50):
    """
    Decorator that adds visual separators before and after the function execution.
    Demonstrates the use of decorators (Requirement 10).
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"\n{char * length}")
            result = func(*args, **kwargs)
            print(f"{char * length}\n")
            return result
        return wrapper
    return decorator

def get_int(prompt: str) -> int:
    """Safely gets an integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a valid integer.")

def get_float(prompt: str) -> float:
    """Safely gets a float input from the user."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a valid floating-point number.")