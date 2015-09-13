import re

# Cut out the movie name from a torrent name
def torrent_to_movie(name):
    # Strings that mark the end of a movie name, and start of meta data
    ends = ["1280p", "1080p", "720p", "r6", "bluray", "bdrip", "brrip", "blu-ray", "blu", "bd", "hd", "hc", "hdtv", "hdcam", "hdscr", "korsub", "extended", "uncut", "unrated", "repack", "r3", "swesub", "ac3", "xvid", "hdrip", "dvdscr", "rc", "dvdrip", "dvdr", "webrip", "rerip", "proper", "hq", "directors", "retail", "boxset", "imax", "x264", "tc", "bdrip720p", "bdrip1080p", "edition", "limited", "french", "swedish", "hindi", "italian", "kor", "nlsubs", "pal", "mkv", "avi", "iso", "mp4", "mpeg", "mov"]
    ends_i = ["iNTERNAL", "CUSTOM", "TS"]  # Case sensitive strings
    ends_double = ["dir cut", "ext cut", "web dl", "dual audio"]
    ends_triple = ["the final cut"]

    # Remove everything after three words followed by a parentesis with a year
    name = re.sub(r"^((?:.*[ \.]){3,}\(\d\d\d\d\)).+", r"\1", name)

    # Remove all non-alpha characters
    words = re.split(r"[^\w'\:]+", name)

    # Loop over all words. As soon as a ending is found, cut to there
    for i, word in enumerate(words):
        if word.lower() in ends or word in ends_i or \
                (i + 1 < len(words) and (word + " " + words[i + 1]).lower() in ends_double) or \
                (i + 2 < len(words) and (word + " " + words[i + 1] + " " + words[i + 2]).lower() in ends_triple):
            words = words[:i]
            break
    name = " ".join(words).lower()

    # Remove unnessesary whitespace
    name = name.strip()

    # Split name and year and return both
    matches = re.split(r" (?=\d{4}$)", name)
    if len(matches) == 2:
        name, year = matches
    else:
        name = matches[0]
        year = None

    return {
        "name": name,
        "year": year,
    }

def remove_bad_torrent_matches(movies):
    # Identify bundles of movies, as opposed to a single movie
    def is_bundle(name):
        # Strings that identify a bundle
        bundle_identifier = [
            "trilogy", "duology", "quadrilogy",
            "movies", "collection", "series", "complete",
            " 1 3 ", " 1 4 ", " 1 5 ", " 1 2 3 "
        ]
        for identifier in bundle_identifier:
            if identifier in name:
                return True

        return False

    def ignore_tv_series(name):
        tv_regex = r"s\d\de\d\d"
        if re.search(tv_regex, name, re.IGNORECASE):
            return True

        if "hdtv" in name:
            return True

        return False

    # Ignore movies that are cams uploaded to the HD section
    def ignore_movies(name):
        # Remove all non-alpha characters
        words = re.split(r"[^\w'-:]+", name.lower())

        # Strings that identify a low quality movie
        ignore_identifier = [
            "cam", "dvdscr", "hc", "hdcam", "hdrip", "hdts", "hqscr", "korsub", "screener", "ts"
        ]
        for identifier in ignore_identifier:
            if identifier in words:
                return True

        return False

    def remove_duplicates_stable(movies):
        nodups = []
        for movie in movies:
            if movie not in nodups:
                nodups.append(movie)

        return nodups

    movies = [movie for movie in movies if not is_bundle(movie["name"])]
    movies = [movie for movie in movies if not ignore_movies(movie["name"])]
    movies = [movie for movie in movies if not ignore_tv_series(movie["name"])]
    movies = remove_duplicates_stable(movies)

    return movies
