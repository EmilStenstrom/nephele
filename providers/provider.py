import copy
import json
from urllib.parse import urlencode

import html5lib
import requests
from application import APPLICATION as APP


class BaseProvider(object):
    # ==== HELPER METHODS ====
    def parse_html(self, url, css_selector, timeout=60, cache=True):
        html = self._http_get(url, timeout=timeout, cache=cache)
        document = html5lib.parse(html)
        results = document.cssselect(css_selector)
        data = [result.text_content() for result in results]
        return data

    def traverse_json(self, data, path):
        if not path:
            return data

        new_data = copy.copy(data)
        for item in path.split("."):
            if item.isdigit():
                item = int(item)

            try:
                new_data = new_data[item]
            except (IndexError, KeyError):
                return {}

        return new_data

    def parse_json(self, url, path=None, timeout=60, cache=True):
        data = self._http_get(url, timeout=timeout, cache=cache)
        data = json.loads(data)
        data = self.traverse_json(data, path)
        return data

    def urlencode(self, data):
        return urlencode(data)

    # ==== PRIVATE METHODS ====
    def _http_get(self, url, timeout=60, cache=True):
        base = requests if not cache else APP.setting("WEBCACHE")
        response = base.get(url, timeout=timeout)
        return response.text
