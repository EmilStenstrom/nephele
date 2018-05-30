from time import sleep

from providers.popularity.provider import PopularityProvider
from utils.torrent_util import remove_bad_torrent_matches, torrent_to_movie

IDENTIFIER = "rarbg"

# API Documentation: https://torrentapi.org/apidocs_v2.txt

class Provider(PopularityProvider):
    def get_popular(self):
        base = "https://torrentapi.org/pubapi_v2.php?"

        token_params = {
            "get_token": "get_token",
            "app_id": "nephele",
        }
        url_token = base + self.urlencode(token_params)
        data_token = self.parse_json(url_token, cache=False)

        sleep(2)

        params = {
            "token": data_token["token"],
            "mode": "list",
            "sort": "seeders",
            "category": "14;48;17;44;45;47;42;46",
            "limit": 100,
            "app_id": "nephele",
        }
        url = base + self.urlencode(params)
        data_movies = self.parse_json(url, cache=False)

        tries = 1
        while "error" in data_movies and tries < 10:
            print("Error returned, retrying in 1 sec")
            sleep(2)
            data_movies = self.parse_json(url, cache=False)
            tries += 1

        names = [item["filename"] for item in data_movies["torrent_results"]]

        movies = [torrent_to_movie(name) for name in names]
        movies = remove_bad_torrent_matches(movies)
        return movies
