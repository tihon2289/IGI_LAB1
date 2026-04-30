"""
Laboratory work #2 (Variant 18)
Program: Text analysis with regular expressions
Version: 1.0
Developer: Your Name
Date: 2026-04-27

Tasks:
- Find words containing digits AND vowel letters.
- Find all arithmetic expressions (two numbers with +,-,*,/).
- General tasks: sentence count, avg length, smileys.
- Save results and archive with zipfile.
"""

import re
import zipfile
import os

def read_text(filepath):
    """Read text from file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("File not found. Using default text.")
        return "Hello world! My phone is 123abc and x=5+3.2, price 9*8. Smile :-) ;--)"

def words_with_digits_and_vowels(text):
    """Return list of words that contain at least one digit and one vowel letter."""
    vowels = set("aeiouyAEIOUY")
    pattern = re.compile(r'\b\w+\b')
    result = []
    for w in pattern.findall(text):
        if re.search(r'\d', w) and any(ch in vowels for ch in w):
            result.append(w)
    return result

def find_arithmetic_expressions(text):
    """Find all simple arithmetic expressions: number operator number.
    Numbers may be negative, integer or float. Operators: + - * /
    Whitespace allowed around operands and operator.
    """
    pattern = r'-?\d+\.?\d*\s*[-+*/]\s*-?\d+\.?\d*'
    return re.findall(pattern, text)

def count_sentences(text):
    """Count sentences (ends with . ! ?)."""
    return len(re.findall(r'[.!?]', text))

def sentence_types(text):
    """Return dict of sentence type counts: declarative, interrogative, imperative.
    Imperative/declarative differentiation simplified: '.' = declarative.
    """
    declar = len(re.findall(r'[.]', text))
    interrog = len(re.findall(r'[?]', text))
    imper = len(re.findall(r'[!]', text))
    return {'declarative': declar, 'interrogative': interrog, 'imperative': imper}

def avg_sentence_length_words(text):
    """Average sentence length in characters (only words characters)."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    total_chars = sum(len(re.sub(r'\s+', '', s)) for s in sentences)
    return total_chars / len(sentences)

def avg_word_length(text):
    """Average word length in characters."""
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return 0
    return sum(len(w) for w in words) / len(words)

def count_smileys(text):
    """Count smileys: ; or : followed by any number of '-' and then one or more
    identical brackets from set (, ), [, ].
    """
    smiley_pattern = r'[:;]-*([\(\)\[\]])\1+'

    return len(re.findall(smiley_pattern, text))

def save_results(results, filepath):
    """Save analysis results to a text file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for key, val in results.items():
            f.write(f"{key}: {val}\n")

def archive_file(filepath, archive_name='result.zip'):
    """Archive file using zipfile and print archive info."""
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(filepath, os.path.basename(filepath))
    print(f"Archived {filepath} -> {archive_name}")
    
    with zipfile.ZipFile(archive_name, 'r') as zf:
        for info in zf.infolist():
            print(f"  {info.filename}, size: {info.file_size}, compressed: {info.compress_size}")

def run_text_analysis():
    """Interactive text analysis."""
    filepath = input("Enter text file path (or press Enter for default): ").strip()
    if not filepath:
        text = "Hello world! My phone is 123abc and x=5+3.2, price 9*8. Smile :-) ;--)"
    else:
        text = read_text(filepath)

    words_dv = words_with_digits_and_vowels(text)
    expressions = find_arithmetic_expressions(text)
    sent_count = count_sentences(text)
    sent_types = sentence_types(text)
    avg_s_len = avg_sentence_length_words(text)
    avg_w_len = avg_word_length(text)
    smileys = count_smileys(text)

    results = {
        "Words with digits and vowels": words_dv,
        "Arithmetic expressions": expressions,
        "Total sentences": sent_count,
        "Sentence types": sent_types,
        "Avg sentence length (chars, words only)": f"{avg_s_len:.2f}",
        "Avg word length": f"{avg_w_len:.2f}",
        "Smileys count": smileys
    }

    print("\n=== Analysis Results ===")
    for k, v in results.items():
        print(f"{k}: {v}")

    out_file = "analysis_result.txt"
    save_results(results, out_file)
    archive_file(out_file)
    print("Results saved and archived.")