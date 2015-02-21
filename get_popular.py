from __future__ import print_function
import sys
from collections import OrderedDict
from importlib import import_module
from settings import POPULARITY_PROVIDERS, MOVIEDATA_PROVIDERS

def main(debug=False):
    popular_list = []
    for provider_path in POPULARITY_PROVIDERS:
        provider_module = import_module(provider_path)
        with provider_module.Provider(debug=debug) as provider:
            print("Fetching from %s" % provider_module.IDENTIFIER)
            popular_list += provider.get_popular()

    data = OrderedDict()
    for provider_path in MOVIEDATA_PROVIDERS:
        provider_module = import_module(provider_path)
        with provider_module.Provider(debug=debug) as provider:
            print("Fetching from %s" % provider_module.IDENTIFIER)
            data = OrderedDict([(name, provider.get_movie_data(name)) for name in popular_list])

    print("=" * 80)
    for name, data in data.items():
        print(name, data)

# Usage:
# python get_popular.py
# python get_popular.py --verbose
if __name__ == "__main__":
    debug = False
    if len(sys.argv) == 2:
        if sys.argv[1] == "--verbose":
            debug = True

    main(debug=debug)
