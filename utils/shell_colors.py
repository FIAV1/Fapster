#!/usr/bin/env python

DEFAULTBG = '\033[49m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINED = '\033[4m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'


def print_red(string, terminator='\n'):
    print(DEFAULTBG + BOLD + RED + string + RESET, end=terminator)


def print_blue(string, terminator='\n'):
    print(DEFAULTBG + BOLD + BLUE + string + RESET, end=terminator)


def print_green(string, terminator='\n'):
    print(DEFAULTBG + BOLD + GREEN + string + RESET, end=terminator)


def print_yellow(string, terminator='\n'):
    print(DEFAULTBG + BOLD + YELLOW + string + RESET, end=terminator)
