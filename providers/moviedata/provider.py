from __future__ import print_function
from providers.provider import BaseProvider

# Subclasses implement a way to get movie data for from a search string
#
# To implement a MoviedataProvider:
#   - Create a new file in moviedata/ and call it provider_[your name].py
#   - Add the path to your file in settings.py, under MOVIEDATA_PROVIDERS
#   - In the new file, Subclass MoviedataProvider and provide a IDENTIFIER
#   - Implement get_movie_data(), returning a dictionary with movie data

class MoviedataProvider(BaseProvider):
    IDENTIFIER = None

    def get_movie_data(self):
        raise NotImplementedError("Subclasses must implement get_movie_data")
