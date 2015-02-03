from __future__ import print_function
import re
import sys

# Cut out the movie name from a torrent name
def movie_title_from_filename(title):
    # Strings that mark the end of a movie name, and start of meta data
    ends = ["1280p", "1080p", "720p", "r6", "bluray", "bdrip", "brrip", "blu-ray", "blu", "bd", "hd", "hdtv", "hdcam", "hdscr", "korsub", "extended", "uncut", "unrated", "repack", "r3", "swesub", "ac3", "xvid", "hdrip", "dvdscr", "rc", "dvdrip", "dvdr", "webrip", "rerip", "proper", "hq", "directors", "retail", "boxset", "x264", "tc", "bdrip720p", "bdrip1080p", "edition", "limited", "french", "swedish", "hindi", "kor", "nlsubs", "pal", "mkv", "avi", "iso", "mp4", "mpeg", "mov"]
    ends_i = ["iNTERNAL", "CUSTOM", "TS"]  # Case sensitive strings
    ends_double = ["dir cut", "ext cut"]
    ends_triple = ["the final cut"]

    # Remove all non-alpha characters
    words = re.split(r"[\W_]+", title)

    # Loop over all words. As soon as a ending is found, cut to there
    for i, word in enumerate(words):
        if word.lower() in ends or word in ends_i or \
                (i+1 < len(words) and (word + " " + words[i+1]).lower() in ends_double) or \
                (i+2 < len(words) and (word + " " + words[i+1] + " " + words[i+2]).lower() in ends_triple):
            words = words[:i]
            break
    title = " ".join(words).lower()

    # Remove unnessesary whitespace
    return title.strip()

# Reduce the number of duplicate movies by removing the year from name
def remove_years(movies):
    return set([("".join(re.split(" \d{4}$", title)).strip()) for title in movies])

# Identify bundles of movies, as opposed to a single movie
def is_bundle(title):
    # Strings that identify a bundle
    bundle_identifier = [
        "trilogy", "duology", "quadrilogy",
        "movies", "collection", "series", "complete",
        " 1 3 ", " 1 4 ", " 1 5 ", " 1 2 3 "
    ]
    for identifier in bundle_identifier:
        if identifier in title:
            return True
    return False

# Separate movies, and movie bundles. Bundles will not be graded.
def separate_movies_from_bundles(mixed):
    movies = [movie for movie in mixed if not is_bundle(movie)]
    bundles = [movie for movie in mixed if is_bundle(movie)]
    return movies, bundles

# Ignore movies that are cams uploaded to the HD section
def ignore_movies(title):
    # Strings that identify a bundle
    ignore_identifier = [
        "CAM", "HDCAM", "HDTS", "Screener", "HQSCR", "DVDScr",
    ]
    for identifier in ignore_identifier:
        if identifier in title:
            return True
    return False 

def filenames_to_search_strings(names):
    names = [title for title in names if not ignore_movies(title)]
    movies = [movie_title_from_filename(title) for title in names]
    movies = remove_years(movies)
    movies = list(set(movies))
    return movies

def print_movies(heading, movie_list):
    if movie_list:
        print(heading)
        print("-" * len(heading))
        if isinstance(movie_list[0], dict):
            max_len = max(map(lambda x: len(x["name"]), movie_list))
            movie_list = sorted(movie_list, key=lambda m: (int(m["grade"]), int(m["commongrade"]), int(m["commongrade_count"])), reverse=True)

            for movie in movie_list:
                grade = movie["grade"] or "-"
                commongrade = movie["commongrade"] or "-"
                name = movie["name"]
                url = movie["url"]

                # If we can't print to your console, remove characters until we can
                enc = sys.stdout.encoding
                try:
                    name.encode(enc)
                except UnicodeEncodeError:
                    name = name.encode("ascii", "replace")

                print((u" %s  %-" + unicode(max_len + 1) + u"s %s (%s)") % (grade, name, url, commongrade))
        else:
            # Bundles are printed as single strings
            for movie in movie_list:
                print(movie)
        print()
