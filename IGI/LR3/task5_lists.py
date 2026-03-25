"""
Purpose: Task 5 - List processing (Variant 12).
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.1
Author: Letkovski Tihon
Date: 2026-03-24
"""

def get_min_abs_index(lst: list) -> int:
    """Finds the index of the minimum by absolute value element."""
    if not lst:
        return 0
        
    min_abs_val = abs(lst[0])
    min_idx = 0
    
    for i in range(1, len(lst)):
        if abs(lst[i]) < min_abs_val:
            min_abs_val = abs(lst[i])
            min_idx = i
            
    return min_idx

def calculate_product_of_positives(lst: list, stop_idx: int) -> float:
    """
    Calculates the product of all positive elements in the list
    up to (but not including) the stop_idx.
    """
    product = 1.0
    has_positives = False
    
    # Итерируемся строго до нужного индекса
    for i in range(stop_idx):
        if lst[i] > 0:
            product *= lst[i]
            has_positives = True
            
    return product if has_positives else 0.0

def calculate_sum_before_index(lst: list, stop_idx: int) -> float:
    """Calculates the sum of elements located before the given index."""
    # Используем срез списка от 0 до stop_idx
    return sum(lst[:stop_idx])

def process_list_data(lst: list):
    """Business logic combining Task 5 requirements."""
    if not lst:
        print("The list is empty.")
        return

    print("\nTarget List:")
    print(lst)
    
    # Находим индекс минимального по модулю элемента один раз
    min_idx = get_min_abs_index(lst)
    print(f"Minimum absolute element is {lst[min_idx]} at index {min_idx}")
    
    # Передаем этот индекс в обе функции
    prod_positives = calculate_product_of_positives(lst, min_idx)
    sum_before_min = calculate_sum_before_index(lst, min_idx)
    
    print(f"Product of positive elements before min abs element: {prod_positives}")
    print(f"Sum of elements before min abs element: {sum_before_min}")