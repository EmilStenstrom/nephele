from importlib import import_module

def update_moviedata(movies, APP):
    for movie in movies:
        imdb_id = APP.NameMapper.get_id(movie["name"])

        for provider_path in APP.setting("MOVIEDATA_PROVIDERS"):
            provider_module = import_module(provider_path)
            provider = provider_module.Provider()
            mapping = provider.get_data_mapping()
            data = APP.Movie.get_data(imdb_id, mapping)
            if imdb_id and data:
                APP.debug_or_dot("Found result in movie db: " + imdb_id)
            else:
                APP.debug_or_dot("Fetching from %s" % provider_module.IDENTIFIER)
                imdb_id, data = provider.get_movie_data(movie)
                APP.NameMapper.update_mapping(movie["name"], imdb_id)
                APP.Movie.update_movie(movie["name"], imdb_id, data)
