#!/usr/bin/env python3
'''Helpers for console interaction'''
import shutil

def center_multiline_string(s):
    '''Returns a multiline string formatted to be centered at current terminal width'''
    term_width = shutil.get_terminal_size((80, 20)).columns
    centered_lines = []
    for line in s.split("\n"):
        padding_left = (term_width - len(line)) // 2
        centered_line = " " * padding_left + line
        centered_lines.append(centered_line)
    return "\n".join(centered_lines)

def get_user_input(prompt):
    '''Wrapper to print prompt and await input'''
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return ".quit"

def print_centered_no_newline(text):
    '''Returns a string formatted to be centered at current terminal width'''
    term_width = shutil.get_terminal_size((80, 20)).columns
    padding_left = (term_width - len(text)) // 2
    print(" " * padding_left + text, end="")
