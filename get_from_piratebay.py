from __future__ import print_function
import sys
from lxml import html
from movie_util import filenames_to_search_strings, separate_movies_from_bundles, print_movies
from http_util import cached_request
from filmtipset_util import get_grades

# Get list of all Highres movies, popular right now, from piratebay
def get_movies(start=0, stop=1, debug=False):
    movies = []
    print("Get pages (%s-%s): " % (start + 1, stop))
    for i in range(start, stop):
        if not debug:
            print(".", end="")
        content = cached_request("http://thepiratebay.se/browse/207/%s/7" % i, "html", debug=debug)
        document = html.document_fromstring(content)
        links = document.cssselect(".detLink")
        movies.extend([link.text_content() for link in links])
    if not debug:
        print()
    print()
    return movies

def main(pages=10, debug=False):
    movies = get_movies(stop=pages, debug=debug)
    movies = filenames_to_search_strings(movies)
    movies, bundles = separate_movies_from_bundles(movies)
    graded = get_grades(movies, debug=debug)

    print_movies("Movies not seen, by grade", sorted(filter(lambda x: x[1] != u'seen', graded), reverse=True))
    print_movies("Bundles, not graded", sorted(bundles))

if __name__ == "__main__":
    debug = False  # Can be set with "get_from_piratebay.py --verbose"
    pages = 10  # Can be set with "get_from_piratebay.py 5"

    if len(sys.argv) >= 2:
        if sys.argv[1] == "--verbose":
            debug = True
        elif int(sys.argv[1]) > 0:
            pages = int(sys.argv[1])
        if len(sys.argv) == 3 and int(sys.argv[2]) > 0:
            pages = int(sys.argv[2])
    main(pages=pages, debug=debug)
