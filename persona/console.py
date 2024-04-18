#!/usr/bin/env python3
'''Helpers for console interaction'''
import shutil
import re
from colored import Fore, Style
import TextJustify

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

def readable_long_string(s):
    return wraptext(s)
    '''Break a long string into multiple lines for readability'''
    words = s.split(' ')
    line = ''
    lines = ''
    for word in words:
        if len(line) + len(word) > 100:
            lines += line + '\n'
            line = '\n\n' + word
        else:
            line += ' ' + word
    lines += line + '\n' # Add the last line
    return lines

def colorize_chat(content):
    '''Colorize chat messages for readability'''
    t = f'{Style.RESET}{Fore.WHITE}' # Styling for plain text
    q = f'{Style.RESET}{Style.BOLD}{Fore.GREEN}' # Styling for quotes
    a = f'{Style.RESET}{Style.ITALIC}{Fore.RED}' # Styling for asterisks
    r = f'{Style.RESET}' # Styling for reset
    asterisk = re.compile(r'([\*])((\{1})*|(.*?[^\\](\{1})*))\1', re.UNICODE)
    content = asterisk.sub(rf'\n\n{a}*\2*{t}\n\n', content)
    quotes = re.compile(r'([\"])((\{1})*|(.*?[^\\](\{1})*))\1', re.UNICODE)
    content = quotes.sub(rf'{q}"\2"{t}', content)
    content = f'{t}{content}{r}'
    return content

def wraptext(content) ->str:
    return TextJustify.justify_text(content, 70, 'left', ' ')
