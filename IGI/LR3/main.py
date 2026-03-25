"""
Purpose: Main program entry point and interactive menu.
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""
from utils import get_int, get_float, ui_separator
import initialization as init
import task1_series
import task2_loops
import task3_text
import task4_string
import task5_lists

@ui_separator(char='=', length=60)
def run_task1():
    print("--- TASK 1: Taylor Series (e^x) ---")
    x = get_float("Enter x value: ")
    eps = get_float("Enter precision (eps) [e.g., 0.0001]: ")
    task1_series.print_series_result(x, eps)

@ui_separator(char='=', length=60)
def run_task2():
    print("--- TASK 2: Loop Analysis ---")
    print("Goal: Count numbers > 12. Stop on 0.")
    result = task2_loops.count_numbers_greater_than_12()
    print(f"Result: {result} numbers were greater than 12.")

@ui_separator(char='=', length=60)
def run_task3():
    print("--- TASK 3: Text Analysis ---")
    text = input("Enter a string to check if it's a binary number: ")
    if task3_text.is_binary_string(text):
        print("The entered string IS a binary number.")
    else:
        print("The entered string IS NOT a binary number.")

@ui_separator(char='=', length=60)
def run_task4():
    print("--- TASK 4: Hardcoded String Analysis ---")
    task4_string.analyze_predefined_string()

@ui_separator(char='=', length=60)
def run_task5():
    print("--- TASK 5: List Processing ---")
    size = get_int("Enter list size: ")
    while size <= 0:
        print("Size must be greater than 0.")
        size = get_int("Enter list size: ")
        
    print("\nChoose initialization method:")
    print("1 - Manual input")
    print("2 - Random generation")
    
    choice = get_int("Your choice: ")
    
    try:
        if choice == 1:
            lst = init.init_list_manual(size)
        elif choice == 2:
            lst = init.init_list_generator(size)
        else:
            print("Invalid choice. Defaulting to Random generation.")
            lst = init.init_list_generator(size)
            
        print("\nTarget List:")
        print(lst)

        if not lst:
            print("The list is empty.")
            return

        min_idx = task5_lists.get_min_abs_index(lst)
        min_val = lst[min_idx]
        print(f"\n[Test] Minimum absolute value is {min_val} at index {min_idx}")
        
        prod_positives = task5_lists.calculate_product_of_positives(lst, min_idx)
        sum_before_min = task5_lists.calculate_sum_before_index(lst, min_idx)
        
        print(f"[Result] Product of positive elements before min abs element: {prod_positives}")
        print(f"[Result] Sum of elements before min abs element: {sum_before_min}")
        
    except Exception as e:
        print(f"Failed to process list: {type(e).__name__} - {e}")

def main_menu():
    """Main menu providing an interactive user interface."""
    while True:
        print("\n" + "#" * 30)
        print("      LABORATORY WORK 3")
        print("         Variant 12")
        print("#" * 30)
        print("1. Task 1 (Taylor Series)")
        print("2. Task 2 (Loop numbers > 12)")
        print("3. Task 3 (Check Binary String)")
        print("4. Task 4 (Predefined Text Analysis)")
        print("5. Task 5 (List Processing)")
        print("0. Exit")
        
        choice = get_int("Select a task to run: ")
        
        if choice == 1:
            run_task1()
        elif choice == 2:
            run_task2()
        elif choice == 3:
            run_task3()
        elif choice == 4:
            run_task4()
        elif choice == 5:
            run_task5()
        elif choice == 0:
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 0 to 5.")

if __name__ == "__main__":
    # Program starts here
    main_menu()