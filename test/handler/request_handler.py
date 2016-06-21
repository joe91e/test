class RequestHandler(object):
    def __init__(self, http_request_handler, cache_request_handler):
        self._http_request_handler = http_request_handler
        self._cache_request_handler = cache_request_handler

    def get(self, url, headers={}):
        if len(url) == 0:
            return "url must be provided!"

        print(url)
        cache_value = self._cache_request_handler.get(url)
        if cache_value is not None and cache_value != "None":
            res = self._cache_request_handler.get(url)
            print("returning from cache")
            #print(res)
            return (res, 200)
        else:
            if len(headers) > 0:
                self._http_request_handler.set_headers(headers)
            self._http_request_handler.set_url(url)
            self._http_request_handler.get()
            res = self._http_request_handler.get_response_content()
            status_code = self._http_request_handler.get_response_status()
            #write to cache
            print("writing to cache")
            self._cache_request_handler.set(url, res)
            print("returning from api call")
            return (res, status_code)
