from __future__ import print_function
from providers.provider import BaseProvider

# Subclasses implement a way to get a list of popular movies in
# the form of a list of search strings
#
# To implement a OutputProvider:
#   - Create a new file in popularity/ and call it provider_[your name].py
#   - Add the path to your file in settings.py, under OUTPUT_PROVIDER
#   - In the new file, Subclass OutputProvider and provide a IDENTIFIER
#   - Implement output(), formatting the movie data like you want

class OutputProvider(BaseProvider):
    IDENTIFIER = None

    def output(self, movie_data):
        raise NotImplementedError("Subclasses must implement output")
