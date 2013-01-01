from __future__ import print_function
import json
from urllib import urlencode
from access_key import ACCESS_KEY, USER_KEY
from http_util import cached_request

# Search for a movie based on name on filmtipset
def search(title, debug=False):
    api = "http://www.filmtipset.se/api/api.cgi"
    options = {
        "accesskey": ACCESS_KEY,
        "returntype": "json",
        "action": "search",
        "usernr": USER_KEY,
        "id": title,
    }
    content = cached_request(api + "?" + urlencode(options), "json", cache_age_days=7, debug=debug)
    results = json.loads(content)
    return results

# Pick the first movie in the search results
def get_first(title, debug=False):
    results = search(title, debug=debug)
    movie = results[0]["data"][0]["hits"][0]["movie"]
    return {
        "grade": movie["grade"]["value"] or "-",
        "commongrade": movie["filmtipsetgrade"]["value"] or "-",
        "type": movie["grade"]["type"],
        "name": movie["name"].strip(),
        "url": movie["url"].strip(),
    }

def get_grades(movies, debug=False):
    grades = []
    print("Get grades (%s-%s): " % (1, len(movies)))
    for movie in movies:
        if not debug:
            print(".", end="")
        grades.append(get_first(movie, debug=debug))
    if not debug:
        print()
    print()
    return grades
