from providers.popularity.provider import PopularityProvider
from utils.torrent_util import torrent_to_movie, remove_bad_torrent_matches

IDENTIFIER = "kickasstorrents"

class Provider(PopularityProvider):
    PAGES_TO_FETCH = 1

    def get_popular(self):
        names = []
        for page in range(Provider.PAGES_TO_FETCH):
            url = "https://kat.cr/usearch/category%%3Ahighres-movies/%s/" % page
            names += self.parse_html(url, "#mainSearchTable .data .cellMainLink", cache=False)

        movies = [torrent_to_movie(name) for name in names]
        movies = remove_bad_torrent_matches(movies)
        return movies
