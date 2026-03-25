"""
Purpose: Task 2 - Loop calculation (Variant 12).
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""
from utils import get_int

def count_numbers_greater_than_12() -> int:
    """
    Accepts integers from keyboard, counts how many are > 12.
    Stops when 0 is entered.
    
    :return: The count of numbers > 12.
    """
    count = 0
    print("Enter integers one by one. Enter 0 to stop.")
    while True:
        num = get_int("Enter number: ")
        if num == 0:
            break
        if num > 12:
            count += 1
    return count