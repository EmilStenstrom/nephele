import json
import requests
from requests.utils import get_unicode_from_response
from requests_cache import CachedSession
from lxml import html as lxml_html
from application import APPLICATION as APP

class BaseProvider(object):
    # ==== HELPER METHODS ====
    def parse_html(self, url, css_selector, timeout=60, cache=True):
        html = self._http_get(url, timeout=timeout, cache=cache)
        document = lxml_html.document_fromstring(html)
        results = document.cssselect(css_selector)
        data = [result.text_content() for result in results]
        return data

    def traverse_json(self, data, path):
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

    def parse_json(self, url, path=None, timeout=60, cache=True):
        data = self._http_get(url, timeout=timeout, cache=cache)
        data = json.loads(data)
        data = self.traverse_json(data, path)
        return data

    # ==== PRIVATE METHODS ====
    def _http_get(self, url, timeout=60, cache=True):
        base = requests
        if cache:
            base = CachedSession(cache_name=APP.setting("WEBCACHE"))

        response = base.get(url, timeout=timeout)
        return get_unicode_from_response(response)
