from __future__ import print_function
import sys
import json
import requests
from requests.utils import get_unicode_from_response
from lxml import html as lxml_html
from utils.cache_util import cached_func

class BaseProvider(object):
    def __init__(self, debug=False):
        self.debug = debug

    # ==== HELPER METHODS ====
    def parse_html(self, url, css_selector):
        if not self.debug:
            print(".", end="")
            sys.stdout.flush()

        def get_and_parse(url):
            html = self._http_get(url)
            document = lxml_html.document_fromstring(html)
            results = document.cssselect(css_selector)
            data = [result.text_content() for result in results]
            return data

        return cached_func(self, url, get_and_parse)

    def parse_json(self, url, path=None):
        if not self.debug:
            print(".", end="")
            sys.stdout.flush()

        def traverse_json(data, path):
            if not path:
                return data

            for item in path.split("."):
                if item.isdigit():
                    item = int(item)

                try:
                    data = data[item]
                except (IndexError, KeyError):
                    return {}

            return data

        def get_and_parse(url):
            data = self._http_get(url)
            data = json.loads(data)
            data = traverse_json(data, path)
            return data

        return cached_func(self, url, get_and_parse)

    def debug_print(self, *args, **kwargs):
        if not self.debug:
            return

        print(*args, **kwargs)

    # ==== PRIVATE METHODS ====
    def _http_get(self, url, timeout=60 * 60):
        response = requests.get(url, timeout=10)
        return get_unicode_from_response(response)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.debug:
            print()
