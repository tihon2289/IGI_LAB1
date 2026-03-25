"""
Purpose: Sequence initialization methods (generator and manual).
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""
import random
from utils import get_float

def init_list_manual(size: int) -> list:
    """
    Initializes a list with user input.
    
    :param size: Number of elements to input.
    :return: List of floats.
    """
    result = []
    print(f"Enter {size} real numbers:")
    for i in range(size):
        result.append(get_float(f"Element {i + 1}: "))
    return result

def init_list_generator(size: int) -> list:
    """
    Initializes a list using a generator with random floats.
    
    :param size: Number of elements to generate.
    :return: List of floats.
    """
    # Using generator expression to create the sequence
    return [round(random.uniform(-50.0, 50.0), 2) for _ in range(size)]