import re

# Cut out the movie name from a torrent name
def movie_title_from_filename(title):
    # Strings that mark the end of a movie name, and start of meta data
    ends = [
        "1080p", "720p", "bluray", "bdrip", "brrip", "blu-ray", "hd", "hdtv",
        "korsub", "extended", "uncut", "unrated", "repack", "r3",
        "swesub", "ac3", "hdrip", "xvid", "dvdscr", "rc", "dvdrip", "dvdr",
        "hq", "boxset", "x264", "tc", "bdrip720p", "bdrip1080p",
        "edition", "limited", "french", "pal",
        "mkv", "avi", "iso", "mp4",
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
def remove_years(movies):
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
def separate_movies_from_bundles(mixed):
    movies = [movie for movie in mixed if not is_bundle(movie)]
    bundles = [movie for movie in mixed if is_bundle(movie)]
    return movies, bundles

def filenames_to_search_strings(names):
    return remove_years([movie_title_from_filename(title) for title in names])
