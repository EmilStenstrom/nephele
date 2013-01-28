from __future__ import print_function
import re

# Cut out the movie name from a torrent name
def movie_title_from_filename(title):
    # Strings that mark the end of a movie name, and start of meta data
    ends = ["1280p", "1080p", "720p", "bluray", "bdrip", "brrip", "blu-ray", "blu", "bd", "hd", "hdtv", "korsub", "extended", "uncut", "unrated", "repack", "r3", "swesub", "ac3", "xvid", "hdrip", "dvdscr", "rc", "dvdrip", "dvdr", "rerip", "proper", "hq", "directors", "retail", "boxset", "x264", "tc", "bdrip720p", "bdrip1080p", "edition", "limited", "french", "swedish", "hindi", "kor", "nlsubs", "pal", "mkv", "avi", "iso", "mp4", "mpeg", "mov"]
    endsi = ["iNTERNAL"]  # Case sensitive strings

    # Remove all non-alpha characters
    words = re.split(r"[\W_]+", title)

    # Loop over all words. As soon as a ending is found, cut to there
    for i, word in enumerate(words):
        if word.lower() in ends or word in endsi:
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

def filenames_to_search_strings(names):
    return remove_years([movie_title_from_filename(title) for title in names])

def print_movies(heading, movie_list):
    if movie_list:
        print(heading)
        print("-" * len(heading))
        if isinstance(movie_list[0], dict):
            movie_list = sorted(movie_list, key=lambda m: (int(m["grade"]), int(m["commongrade"]), int(m["commongrade_count"])), reverse=True)
            max_len = max(map(lambda x: len(x["name"]), movie_list))
            for movie in movie_list:
                grade = movie["grade"] or "-"
                common = movie["commongrade"] or "-"
                name = movie["name"]
                url = movie["url"]
                print(("%s (%s) %-" + str(max_len + 1) + "s %s") % (grade, common, name, url))
        else:
            for movie in movie_list:
                print(movie)
        print()
