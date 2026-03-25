"""
Purpose: Task 3 - Text analysis (Variant 12).
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""

def is_binary_string(text: str) -> bool:
    """
    Determines if a given string represents a binary number.
    Does not use regular expressions.
    
    :param text: String to check.
    :return: True if binary, False otherwise.
    """
    text = text.strip()
    if not text:
        return False
        
    for char in text:
        if char not in ('0', '1'):
            return False
    return True