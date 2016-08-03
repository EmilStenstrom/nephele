from providers.popularity.provider import PopularityProvider
from utils.torrent_util import torrent_to_movie, remove_bad_torrent_matches

IDENTIFIER = "YIFY"

class Provider(PopularityProvider):
    PAGES_TO_FETCH = 10

    def get_popular(self):
        movies = []
        base = "https://yts.ag/browse-movies"

        for page in range(Provider.PAGES_TO_FETCH):
            url = base + ("?page=%s" % page if page > 1 else "")
            result = self.parse_html(url, ".browse-movie-title, .browse-movie-year", cache=False)
            movies += [{
                "name": movie,
                "is_bad": False,
                "year": year,
            } for movie, year in zip(result[::2], result[1::2])]

        # No cleanup needed, YTS is curated
        return movies
