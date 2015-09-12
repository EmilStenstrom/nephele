"""Nephele - Finding movies to watch on the internet is easy,
finding GOOD movies to watch is hard. Let Nephele, the greek
nymph of the clouds, help you.

Usage:
    nephele.py get_popular [--debug]
    nephele.py get_grades <directory> [--debug]
    nephele.py clear <name> [--debug]

Options:
    -h --help     Show this screen.
    --debug       Print debug information.

"""
from docopt import docopt
import importlib

if __name__ == '__main__':
    arguments = docopt(__doc__)
    command_str = [key for key, value in arguments.items() if value][0]
    command = importlib.import_module("commands." + command_str)
    command.main(arguments)
