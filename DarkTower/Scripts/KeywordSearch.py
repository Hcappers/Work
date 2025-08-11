#!/usr/bin/env python3
"""
:: Description: Searches an input text file for lines containing a keyword
               or multiple keywords from a file.
:: Usage:       KeywordSearch.py [input_file]
:: Written by:  Alex Cappers on 2025-08-02 (modified)
"""

import os
import sys
import argparse
import re

# ANSI color codes
class Colors:
    NOTE   = '\033[93m'  # yellow
    ERROR  = '\033[91m'  # red
    OK     = '\033[92m'  # green
    ACTION = '\033[96m'  # cyan
    RESET  = '\033[0m'

def eprint(msg, color=Colors.ERROR):
    print(f"{color}{msg}{Colors.RESET}", file=sys.stderr)

def sprint(msg, color=Colors.OK):
    print(f"{color}{msg}{Colors.RESET}")

def normalize(s: str) -> str:
    """Lowercase and strip spaces/hyphens for comparison."""
    return re.sub(r'[-\s]+', '', s).lower()

def prompt_input_file(arg):
    if arg:
        return arg
    sprint("[NOTE] Please enter the path to the text file to search:", Colors.NOTE)
    return input().strip()

def prompt_result_filename():
    sprint("[NOTE] Enter the name for the result file (without extension):", Colors.NOTE)
    name = input().strip().replace(" ", "_")
    return f"{name}.txt"

def prompt_mode():
    sprint("[NOTE] Single keyword (enter 1) or file of keywords (enter 2)?", Colors.NOTE)
    return input().strip()

def load_keywords_file(path):
    try:
        with open(path, encoding='utf-8') as f:
            kws = [line.strip() for line in f
                   if (kw := line.strip()) and not kw.startswith("#")]
        return kws
    except Exception as e:
        eprint(f"[ERROR] Could not read keywords file '{path}': {e}")
        sys.exit(1)

def filter_lines(input_path, keywords, output_path):
    try:
        with open(input_path, encoding='utf-8') as infile, \
             open(output_path, 'a', encoding='utf-8') as outfile:
            for line in infile:
                norm_line = normalize(line)
                if any(normalize(kw) in norm_line for kw in keywords):
                    outfile.write(line)
    except Exception as e:
        eprint(f"[ERROR] File error: {e}")
        sys.exit(1)

def main():
    # 1) parse optional input-file argument
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("input_file", nargs="?", help=argparse.SUPPRESS)
    args, _ = parser.parse_known_args()

    # 2) get the input text file
    input_file = prompt_input_file(args.input_file)
    if not os.path.isfile(input_file):
        eprint(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    # 3) set up the result file next to this script
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    result_file = os.path.join(script_dir, prompt_result_filename())
    try:
        # truncate or create
        open(result_file, 'w', encoding='utf-8').close()
        sprint(f"[OK] Result file created: {result_file}", Colors.OK)
    except Exception as e:
        eprint(f"[ERROR] Could not create result file: {e}")
        sys.exit(1)

    # 4) choose mode
    mode = prompt_mode()
    if mode == "1":
        sprint("[NOTE] Please enter the keyword to search for:", Colors.NOTE)
        kw = input().strip()
        sprint(f"[ACTION] Filtering lines for '{kw}'...", Colors.ACTION)
        filter_lines(input_file, [kw], result_file)
        sprint(f"[OK] Done. Matches written to '{result_file}'.", Colors.OK)

    elif mode == "2":
        sprint("[NOTE] Please enter the path to your keywords file:", Colors.NOTE)
        kw_path = input().strip()
        if not os.path.isfile(kw_path):
            eprint(f"[ERROR] Keywords file not found: {kw_path}")
            sys.exit(1)

        keywords = load_keywords_file(kw_path)
        if not keywords:
            eprint("[ERROR] No keywords loaded from file.")
            sys.exit(1)

        for kw in keywords:
            sprint(f"[ACTION] Filtering lines for '{kw}'...", Colors.ACTION)
            filter_lines(input_file, [kw], result_file)

        sprint(f"[OK] All done. Matches written to '{result_file}'.", Colors.OK)

    else:
        eprint("[ERROR] Invalid option—enter 1 or 2.")
        sys.exit(1)

if __name__ == "__main__":
    main()