from providers.popularity.provider import PopularityProvider
from utils.torrent_util import remove_bad_torrent_matches, torrent_to_movie

IDENTIFIER = "kickasstorrents"

class Provider(PopularityProvider):
    PAGES_TO_FETCH = 3

    def get_popular(self):
        names = []
        base = "https://kickasstorrents.to/highres-movies/"
        # New mirrors can be found at https://thekickasstorrents.com/

        for page in range(Provider.PAGES_TO_FETCH):
            if page == 0:
                url = base
            else:
                url = base + "%s/" % (page + 1)

            names += self.parse_html(url, "#mainSearchTable .data .cellMainLink", cache=False)

        movies = [torrent_to_movie(name) for name in names]
        movies = remove_bad_torrent_matches(movies)
        return movies
