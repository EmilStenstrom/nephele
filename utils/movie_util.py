from importlib import import_module

def update_moviedata(movies, APP):
    for movie in movies:
        for provider_path in APP.setting("MOVIEDATA_PROVIDERS"):
            provider_module = import_module(provider_path)
            provider = provider_module.Provider()
            mapping = provider.get_data_mapping()
            missing_keys = APP.Movie.has_all_fields(movie, mapping)
            if not missing_keys:
                APP.debug_or_dot("Found and has correct fields for %s: %s" % (provider_module.IDENTIFIER, movie["name"]))
                continue

            APP.debug("Not found \"%s\", missing keys: %s" % (movie["name"], ", ".join(missing_keys)))
            APP.debug_or_dot("Fetching from %s" % (provider_module.IDENTIFIER))
            data = provider.fetch_movie_data(movie)
            if not data:
                continue

            APP.Movie.update_movie(movie, data)
