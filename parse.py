from __future__ import print_function
import sys
import re
import os
import hashlib
import requests
import json
import codecs
from datetime import datetime
from time import sleep
from lxml import html
from urllib import urlencode
from access_key import ACCESS_KEY, USER_KEY

DEBUG = False # Can be set with --verbose

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
    print("Get pages (%s-%s): " % (start+1, stop))
    for i in range(start, stop):
        if not DEBUG: print(".", end="")
        content = cached_request("http://thepiratebay.org/browse/207/%s/7" % i, "html")
        document = html.document_fromstring(content)
        links = document.cssselect(".detLink")
        movies.extend([(link.get("href"), link.text_content()) for link in links])
    if not DEBUG: print()
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
        if not DEBUG: print(".", end="")
        grades.append(get_first(movie))
    if not DEBUG: print()
    print()
    return set(grades)

# Cut out the movie name from a torrent name
def strip_title(title):
    # Strings that mark the end of a movie name, and start of meta data
    ends = [
        "1080p", "720p", "bluray", "bdrip", "brrip", "hd",
        "korsub", "extended", "uncut", "unrated", "repack",
        "swesub", "ac3", "hdrip", "xvid", "dvdscr", "rc",
        "hq", "boxset", "x264", "tc", "bdrip720p", "bdrip1080p",
        "edition"
    ]

    # Remove all non-alpha characters
    words = re.split(r"[\W_]+", title.lower())

    # Loop over all words. As soon as a ending is found, cut to there
    for i, word in enumerate(words):
        if word in ends:
            words = words[:i]
            break
    title = " ".join(words).lower()

    # Remove unnessesary whitespace
    return title.strip()

# Reduce the number of duplicate movies by removing the year from name
def unique(movies):
    return set([("".join(re.split(" \d{4}$", title)).strip()) for title in movies])

# Identify bundles of movies, as opposed to a single movie
def is_bundle(title):
    # Strings that identify a bundle
    bundle_identifier = [
        "trilogy", "duology", "quadrilogy",
        "movies", "collection", "series", "complete",
        " 1 3 ", " 1 4 ", " 1 5 "
    ]
    for identifier in bundle_identifier:
        if identifier in title:
            return True
    return False

# Separate movies, and movie bundles. Bundles will not be graded.
def partition(mixed):
    movies = [movie for movie in mixed if not is_bundle(movie)]
    bundles = [movie for movie in mixed if is_bundle(movie)]
    return movies, bundles

# Print out debug messages, if run in verbose mode
def debug(message):
    if DEBUG:
        print(message)

def out(header, collection):
    if not collection:
        return

    print(header)
    print("-"*len(header))
    if isinstance(collection[0], tuple):
        max_len = min(60, len(max(collection, key=lambda x: len(x[2]))[2]))
        for item in collection:
            num = "%-2s" % item[0]
            name = ("%-" + str(max_len + 1) + "s") % item[2]
            link = item[3]
            try:
                print(num, name, link)
            except UnicodeEncodeError:
                print(num, name.encode("latin-1", link))
    else:
        for item in collection:
            print(item)
    print()

def main():
    movies = unique([strip_title(title) for url, title in get_movies(stop=10)])
    movies, bundles = partition(movies)
    graded = get_grades(movies)

    out("Movies not seen, by grade", sorted(filter(lambda x: x[1] != u'seen', graded), reverse=True))
    out("Bundles, not graded", sorted(bundles))

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--verbose":
        DEBUG = True
    main()
