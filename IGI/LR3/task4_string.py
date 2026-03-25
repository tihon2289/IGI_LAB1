"""
Purpose: Task 4 - Hardcoded string analysis (Variant 12).
Lab: 3
Title: Standard data types, collections, functions, modules.
Version: 1.0
Author: Letkovski Tihon
Date: 2026-03-24
"""
import string

TARGET_TEXT = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

def count_uppercase_letters(text: str) -> int:
    """Counts uppercase letters in the text."""
    return sum(1 for char in text if char.isupper())

def find_first_word_with_z(text: str) -> tuple:
    """
    Finds the first word containing 'z' and its order number (1-based).
    Ignores punctuation.
    """
    clean_text = text.translate(str.maketrans('', '', string.punctuation))
    words = clean_text.split()
    
    for index, word in enumerate(words):
        if 'z' in word.lower():
            return word, index + 1
    return None, -1

def exclude_words_starting_with_a(text: str) -> str:
    """
    Returns the text excluding words that start with the letter 'a'.
    Preserves basic punctuation attached to other words.
    """
    words = text.split()
    filtered_words = []
    
    for word in words:
        # Strip punctuation just for the check
        clean_word = word.strip(string.punctuation)
        if clean_word and not clean_word.lower().startswith('a'):
            filtered_words.append(word)
            
    return " ".join(filtered_words)

def analyze_predefined_string():
    """Executes all business logic for Task 4."""
    print("Original text:")
    print(TARGET_TEXT, "\n")
    
    # a)
    uppercase_count = count_uppercase_letters(TARGET_TEXT)
    print(f"a) Number of uppercase letters: {uppercase_count}")
    
    # b)
    word, index = find_first_word_with_z(TARGET_TEXT)
    if word:
        print(f"b) First word with 'z': '{word}' at position {index}")
    else:
        print("b) There are no words containing the letter 'z' in the text.")
        
    # c)
    filtered_text = exclude_words_starting_with_a(TARGET_TEXT)
    print("c) Text without words starting with 'a':")
    print(filtered_text)