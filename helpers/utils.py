"""
Copyright © Basi

Github: https://github.com/basiiii
Website: https://basi.is-a.dev/
Discord: basi__

🏛️ Private discord bot for Warframe Arbitrations made with Discord.py.
https://discord.gg/arbitrations
"""

import os
import sys
from termcolor import colored

"""
Define special colour print to console.

fatal = fatal error
warning = warning error
info = information
"""
def print_fatal(x): return print(colored(x, 'yellow', 'on_red'))
def print_warning(x): return print(colored(x, 'yellow', 'on_black'))
def print_info(x): return print(colored(x, 'black', 'on_blue'))

def get_config_path(filename):
    """Get path to the config file.

    Args:
        filename (String): File name.

    Returns:
        String: File path.
    """
    if getattr(sys, 'frozen', False):
        # If the application is run as a frozen exe
        application_path = os.path.dirname(sys.executable)
    else:
        # If the application is run as a script
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, filename)
