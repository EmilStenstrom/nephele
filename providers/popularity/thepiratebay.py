from providers.popularity.provider import PopularityProvider
from utils.torrent_util import torrent_to_movie, remove_bad_torrent_matches
from urllib.parse import quote

IDENTIFIER = "thepiratebay"

class Provider(PopularityProvider):
    PAGES_TO_FETCH = 3

    def get_popular(self):
        names = []
        query = quote("720p | 1080p | DVDRip")
        for page in range(Provider.PAGES_TO_FETCH):
            url = "https://thepiratebay.org/search/%s/%s/99/207" % (query, page)
            names += self.parse_html(url, ".detLink", cache=False)

        movies = [torrent_to_movie(name) for name in names]
        movies = remove_bad_torrent_matches(movies)
        return movies
