#!/usr/bin/env python -u

"""

Nephele - Finding movies to watch on the internet is easy,
finding GOOD movies to watch is hard. Let Nephele, the greek
nymph of the clouds, help you.

Usage:
    nephele.py get_popular [--limit=<n>] [--filter=<spec>] [--debug]
    nephele.py get_grades <directory> [--limit=<n>] [--filter=<spec>] [--debug]
    nephele.py clear <name> [--debug]

Options:
    -h --help        Show this screen.
    --debug          Print debug information.
    --limit=<n>      Limit number of returned hits [default: 10]
    --filter=<spec>  Filter resulting movies on this specification

                     <spec> takes a comma separated list of movie field names,
                     followed by an operator and a value to compare to.

                     Valid operators are:
                        * Equal: == (if the value is a list, equal means "contains" instead)
                        * Not equal: == (if the value is a list, not equal means "does not contain" instead)
                        * Larger than: >, Less than: <
                        * Larger than or equal: >=, Less than or equal: <=

                     Examples:
                        * --filter="imdb_rating>4.5"
                        * --filter="filmtipset_my_grade>=4"
                        * --filter="imdb_rating>5,filmtipset_my_grade>=4"
                        * --filter="genre==Romance"
                        * --filter="genre!=Animation"

"""
from docopt import docopt
import importlib

if __name__ == '__main__':
    arguments = docopt(__doc__)
    command_str = [key for key, value in arguments.items() if value][0]
    command = importlib.import_module("commands." + command_str)
    command.main(arguments)
