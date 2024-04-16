import re
from colored import Fore, Back, Style



def colorize_chat(content):
    t = f'{Style.RESET}{Fore.WHITE}' # Styling for plain text
    q = f'{Style.RESET}{Style.BOLD}{Fore.GREEN}' # Styling for quotes
    a = f'{Style.RESET}{Style.ITALIC}{Fore.RED}' # Styling for asterisks
    r = f'{Style.RESET}' # Styling for reset
    
    asterisk = re.compile(r'([\*])((\{1})*|(.*?[^\\](\{1})*))\1', re.UNICODE)
    content = asterisk.sub(rf'{a}*\2*{t}', content)
    quotes = re.compile(r'([\"])((\{1})*|(.*?[^\\](\{1})*))\1', re.UNICODE)
    content = quotes.sub(rf'{q}"\2"{t}', content)
    content = f'{t}{content}{r}'
    return content