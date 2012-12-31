from __future__ import print_function
import sys
import os
import hashlib
import requests
import json
from datetime import datetime
import codecs
from time import sleep
from lxml import html
from urllib import urlencode
from access_key import ACCESS_KEY, USER_KEY
from movie_util import filenames_to_search_strings, separate_movies_from_bundles

DEBUG = False  # Can be set with "parse.py --verbose"
PAGES = 10  # Can be set with "parse.py 5"

# Fetch an URL and cache the response cache_age_days
def cached_request(url, type, cache_age_days=1):
    BASE_PATH = "cache"
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    url_hash = hashlib.md5(url).hexdigest()
    cache_path = os.path.join(BASE_PATH, "%s_%s.%s" % (type, url_hash, type))
    cache_date = datetime.fromtimestamp(os.path.getmtime(cache_path)) if os.path.exists(cache_path) else 0

    if os.path.exists(cache_path) and (datetime.now() - cache_date).days < cache_age_days:
        debug("CACHE: %s" % url)
        with codecs.open(cache_path, "r", "utf-8") as f:
            content = f.read()
    else:
        debug("WEB: %s" % url)
        r = requests.get(url, timeout=5)
        if type == "json":
            content = json.dumps(json.loads(unicode(r.content, "iso-8859-15")), indent=4)
        else:
            content = r.content
        with codecs.open(cache_path, "w", "utf-8") as f:
            f.write(content)
        # Use a delay to prevent DoS
        sleep(0.5)
    return content

# Get list of all Highres movies, popular right now, from piratebay
def get_movies(start=0, stop=1):
    movies = []
    print("Get pages (%s-%s): " % (start + 1, stop))
    for i in range(start, stop):
        if not DEBUG:
            print(".", end="")
        content = cached_request("http://thepiratebay.se/browse/207/%s/7" % i, "html")
        document = html.document_fromstring(content)
        links = document.cssselect(".detLink")
        movies.extend([(link.get("href"), link.text_content()) for link in links])
    if not DEBUG:
        print()
    print()
    return movies

# Search for a movie based on name on filmtipset
def search(title):
    api = "http://www.filmtipset.se/api/api.cgi"
    options = {
        "accesskey": ACCESS_KEY,
        "returntype": "json",
        "action": "search",
        "usernr": USER_KEY,
        "id": title,
    }
    content = cached_request(api + "?" + urlencode(options), "json", cache_age_days=7)
    results = json.loads(content)
    return results

# Pick the first movie in the search results
def get_first(title):
    results = search(title)
    movie = results[0]["data"][0]["hits"][0]["movie"]
    grade = movie["grade"]["value"] or "-"
    type = movie["grade"]["type"]
    name = movie["name"].strip()
    url = movie["url"].strip()
    return (grade, type, name, url)

def get_grades(movies):
    grades = []
    print("Get grades (%s-%s): " % (1, len(movies)))
    for movie in movies:
        if not DEBUG:
            print(".", end="")
        grades.append(get_first(movie))
    if not DEBUG:
        print()
    print()
    return set(grades)

# Print out debug messages, if run in verbose mode
def debug(message):
    if DEBUG:
        print(message)

def out(header, collection):
    if collection:
        print(header)
        print("-" * len(header))
        if isinstance(collection[0], tuple):
            max_len = len(max(collection, key=lambda x: len(x[2]))[2])
            for item in collection:
                print("%-2s" % item[0], ("%-" + str(max_len + 1) + "s") % item[2], item[3])
        else:
            for item in collection:
                print(item)
        print()

def main():
    movies = get_movies(stop=PAGES)
    movies = filenames_to_search_strings(movies)
    movies, bundles = separate_movies_from_bundles(movies)
    graded = get_grades(movies)

    out("Movies not seen, by grade", sorted(filter(lambda x: x[1] != u'seen', graded), reverse=True))
    out("Bundles, not graded", sorted(bundles))

# Possible calls:
# parse.py --verbose
# parse.py 10
# parse.py --verbose 10
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "--verbose":
            DEBUG = True
        elif int(sys.argv[1]) > 0:
            PAGES = int(sys.argv[1])
        if len(sys.argv) == 3 and int(sys.argv[2]) > 0:
            PAGES = int(sys.argv[2])
    main()
