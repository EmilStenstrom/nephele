from providers.popularity.provider import PopularityProvider
from utils.torrent_util import remove_bad_torrent_matches, torrent_to_movie

IDENTIFIER = "netflix"

class Provider(PopularityProvider):
    def get_popular(self):
        country = "se"
        url = f"https://www.finder.com/{country}/netflix-movies"
        data = self.parse_html(url, 'tbody td[data-title="Title"] b, tbody td[data-title="Year of release"]', cache=False)
        movies = [
            {
                "name": movie,
                "is_bad": False,
                "year": year,
            }
            for movie, year in zip(data[::2], data[1::2])
        ]

        return movies
