from __future__ import print_function
import os
import hashlib
import requests
import json
from datetime import datetime
import codecs
from time import sleep

requests.adapters.DEFAULT_RETRIES = 3

# Fetch an URL and cache the response cache_age_days
def cached_request(url, type, cache_age_days=1, debug=False):
    BASE_PATH = "cache"
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

    url_hash = hashlib.md5(url).hexdigest()
    cache_path = os.path.join(BASE_PATH, "%s_%s.%s" % (type, url_hash, type))
    cache_date = datetime.fromtimestamp(os.path.getmtime(cache_path)) if os.path.exists(cache_path) else 0

    if os.path.exists(cache_path) and (datetime.now() - cache_date).days < cache_age_days:
        if debug:
            print("CACHE: %s" % url)
        with codecs.open(cache_path, "r", "utf-8") as f:
            content = f.read()
    else:
        if debug:
            print("WEB: %s" % url)
        r = requests.get(url, timeout=10)
        r.encoding = "utf-8"
        if type == "json":
            content = json.dumps(json.loads(unicode(r.content, "iso-8859-15")), indent=4)
        else:
            content = r.content
        try:
            with codecs.open(cache_path, "w", "utf-8") as f:
                f.write(content)
        except UnicodeDecodeError:
            os.remove(cache_path)
            print("Failed reading url because of encoding error: %s" % url, end="")

        # Use a delay to prevent DoS
        sleep(0.5)
    return content
