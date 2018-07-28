import re
from datetime import datetime
from difflib import SequenceMatcher


# Cut out the movie name from a torrent name
def torrent_to_movie(name):
    # Strings that mark the end of a movie name, and start of meta data
    ends = ["1280p", "1080p", "720p", "r6", "bluray", "bdrip", "brrip", "blu-ray", "blu", "bd", "hd", "hc", "hdtv", "hdcam", "hdscr", "hdtc", "korsub", "extended", "uncut", "unrated", "repack", "r3", "swesub", "ac3", "xvid", "hdrip", "dvdscr", "rc", "dvdrip", "dvdr", "webrip", "rerip", "proper", "hq", "directors", "retail", "boxset", "imax", "x264", "tc", "bdrip720p", "bdrip1080p", "edition", "limited", "french", "swedish", "hindi", "italian", "malayalam", "kor", "eng", "nlsubs", "pal", "mkv", "avi", "iso", "mp4", "mpeg", "mov", "japanese", "amzn"]
    ends_i = ["iNTERNAL", "CUSTOM", "TS", "MULTi", "EC"]  # Case sensitive strings
    ends_double = ["dir cut", "ext cut", "web dl", "dual audio", "extended cut", "final cut"]
    ends_triple = ["the final cut"]

    # Remove everything after three words followed by a parentesis with a year
    name = re.sub(r"^((?:.*[ \.]){3,}\(\d\d\d\d\)).+", r"\1", name)

    # Remove all non-alpha characters
    raw_words = re.split(r"[^\w'\:]+", name, flags=re.UNICODE)

    # Loop over all words. As soon as a ending is found, cut to there
    words = raw_words
    for i, word in enumerate(words):
        if word.lower() in ends or word in ends_i or \
                (i + 1 < len(words) and (word + " " + words[i + 1]).lower() in ends_double) or \
                (i + 2 < len(words) and (word + " " + words[i + 1] + " " + words[i + 2]).lower() in ends_triple):
            words = words[:i]
            break
    name = " ".join(words).lower()

    # Remove unnessesary whitespace
    name = name.strip()

    # If name ends with a movie release year, return year separately
    year = None
    match = re.match(r"^(?P<name>.+) (?P<year>\d{4})$", name)
    if match and 1900 < int(match.group("year")) <= datetime.now().year:
        name = match.group("name")
        year = match.group("year")

    return {
        "name": name,
        "year": year,
        "is_bad": is_tv(raw_words) or is_cam(raw_words) or is_bundle(raw_words),
    }

def is_tv(words):
    tv_regex = r"s\d\de\d\d"
    tokens = [word.lower() for word in words]

    for word in tokens:
        if re.search(tv_regex, word, re.IGNORECASE):
            return True

    if "hdtv" in tokens:
        return True

    return False

# Ignore movies that are cams uploaded to the HD section
def is_cam(words):
    # Strings that identify a low quality movie
    ignore_identifier = [
        "cam", "dvdscr", "hc", "hdcam", "hdrip", "hdts", "hdtc", "hqscr", "korsub", "screener", "ts"
    ]
    tokens = [word.lower() for word in words]
    for identifier in ignore_identifier:
        if identifier in tokens:
            return True

    return False

# Identify bundles of movies, as opposed to a single movie
def is_bundle(words):
    # Strings that identify a bundle
    bundle_identifier = [
        "trilogy", "duology", "quadrilogy",
        "movies", "collection", "series", "complete",
        " 1 3 ", " 1 4 ", " 1 5 ", " 1 2 3 "
    ]
    tokens = [word.lower() for word in words]
    for identifier in bundle_identifier:
        if identifier in tokens:
            return True

    return False

def remove_bad_torrent_matches(movies):
    def remove_duplicates_stable(movies):
        nodups = []
        for movie in movies:
            too_similar = False
            for existing_movie in nodups:
                matcher = SequenceMatcher(a=movie["name"], b=existing_movie["name"])
                is_over_95_percent_similar = (matcher.ratio() > 0.95)

                is_prefix_of_existing = \
                    movie["name"].startswith(existing_movie["name"]) or \
                    existing_movie["name"].startswith(movie["name"])

                if is_over_95_percent_similar or is_prefix_of_existing:

                    # Does the movie exist, but with a different year?
                    if not movie["year"] or movie["year"] == existing_movie["year"]:
                        too_similar = True
                        break

            if not too_similar:
                nodups.append(movie)

            elif len(movie["name"]) > len(existing_movie["name"]):
                nodups.remove(existing_movie)
                nodups.append(movie)

        return nodups

    movies = [movie for movie in movies if not movie["is_bad"]]
    movies = remove_duplicates_stable(movies)

    return movies
