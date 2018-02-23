from providers.provider import BaseProvider

# Subclasses implement a way to get movie data for from a search string
#
# To implement a MoviedataProvider:
#   - Create a new file in moviedata/ and call it provider_[your name].py
#   - Add the path to your file in settings.py, under MOVIEDATA_PROVIDERS
#   - In the new file, Subclass MoviedataProvider and provide a IDENTIFIER
#   - Implement get_url() if your backend makes external HTTP requests
#       - It's used to purge the HTTP cache later
#   - Implement fetch_movie_data() that recieves a dict with a name and possibly a year
#       -  It returns a dictionary with movie data
#   - Implement get_data_fields()
#       -  It returns a dictionary mapping db fields to data that
#          this provider has added to data

class MoviedataProvider(BaseProvider):
    IDENTIFIER = None

    def get_url(self, movie):
        raise NotImplementedError("Subclasses must implement get_url")

    def fetch_movie_data(self, movie):
        raise NotImplementedError("Subclasses must implement fetch_movie_data")

    def get_data_mapping(self):
        raise NotImplementedError("Subclasses must implement get_data_mapping")

    # ==== HELPER METHODS ====
    def transform_data(self, data):
        if not data:
            return data

        out_data = {}
        mapping = self.get_data_mapping()
        for to_field, from_field in mapping.items():
            if callable(from_field):
                out_data[to_field] = from_field(data)
            elif isinstance(from_field, str):
                out_data[to_field] = self.traverse_json(data, path=from_field)
            else:
                assert False, "Unknown type for: " + repr(from_field)

        return out_data
