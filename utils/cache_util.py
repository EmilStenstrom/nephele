from __future__ import print_function
from datetime import datetime, timedelta
from tinydb import where
from settings import db_cache

def _date_to_str(d):
    return d.replace(microsecond=0).isoformat()

# Fetch an URL and cache the response cache_age_days
def cached_func(klass, key, func, cache_table=db_cache, cache_timeout=60 * 60):
    now = datetime.now()

    # FIXME: Account for timeout
    record = cache_table.get(where("key") == key)
    if record:
        klass.debug_print("Found in cache:", key)
        return record["value"]

    klass.debug_print("Calling func for:", key)
    value = func(key)
    cache_table.insert({
        "key": key,
        "value": value,
        "timeout": _date_to_str(now + timedelta(seconds=cache_timeout)),
    })
    return value
