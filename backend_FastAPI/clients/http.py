from urllib import request, parse

import logging
logger = logging.getLogger(__name__)

class HTTPClient:
    @staticmethod
    def fetch(url, params=None, data=None):
        if params:
            query_string = parse.urlencode(params)
            url = f"{url}?{query_string}"

        req = request.Request(url, data=data)

        with request.urlopen(req) as res:
            logger.info(f"Fetching URL: {url}")
            return res.read()