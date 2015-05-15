from providers.popularity.provider import PopularityProvider
from utils.torrent_util import torrent_to_search_string, remove_bad_torrent_matches

IDENTIFIER = "Torrentz"

class Provider(PopularityProvider):
    PAGES_TO_FETCH = 1

    def get_popular(self):
        results = []
        for page in range(Provider.PAGES_TO_FETCH):
            terms = ["movies", "hd", "-xxx", "-porn"]
            url = "https://torrentz.eu/search?q=%s&p=%s" % (
                "+".join(terms), page
            )
            results += self.parse_html(url, ".results dt a")

        results = remove_bad_torrent_matches(results)
        results = [torrent_to_search_string(name) for name in results]
        return results
