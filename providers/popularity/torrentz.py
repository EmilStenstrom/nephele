from providers.popularity.provider import PopularityProvider
from utils.torrent_util import torrent_to_movie, remove_bad_torrent_matches

IDENTIFIER = "Torrentz"

class Provider(PopularityProvider):
    PAGES_TO_FETCH = 1

    def get_popular(self):
        names = []
        for page in range(Provider.PAGES_TO_FETCH):
            terms = ["movies", "hd", "-xxx", "-porn"]
            url = "https://torrentz.eu/search?q=%s&p=%s" % (
                "+".join(terms), page
            )
            names += self.parse_html(url, ".results dt a")

        movies = [torrent_to_movie(name) for name in names]
        movies = remove_bad_torrent_matches(movies)
        return movies
