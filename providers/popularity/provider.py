from providers.provider import BaseProvider

# Subclasses implement a way to get a list of popular movies in
# the form of a list of search strings
#
# To implement a PopularityProvider:
#   - Create a new file in popularity/ and call it provider_[your name].py
#   - Add the path to your file in settings.py, under POPULARITY_PROVIDER
#   - In the new file, Subclass PopularityProvider and provide a IDENTIFIER
#   - Implement get_popular(), returning a list of movie names (as strings)

class PopularityProvider(BaseProvider):
    IDENTIFIER = None

    def get_popular(self):
        raise NotImplementedError("Subclasses must implement get_popular")
