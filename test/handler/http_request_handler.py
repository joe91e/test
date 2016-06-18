from abc import ABCMeta, abstractmethod
import requests
import json


class HttpRequestAbstract(object):
    __metaclass__ = ABCMeta

    def __init__(self, request):
        self._request = request
        self._headers = {'content-type': 'application/json'}
        self._response = None
        self._url = None

    @abstractmethod
    def set_headers(self, headers):
        pass

    @abstractmethod
    def get_headers(self):
        pass

    @abstractmethod
    def get_last_request(self):
        pass

    @abstractmethod
    def post(self, data=None, **kwargs):
        pass

    @abstractmethod
    def put(self, data=None, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def get_response_content(self):
        pass

    @abstractmethod
    def get_response_status(self):
        pass

    @abstractmethod
    def set_url(self, url):
        pass

    @abstractmethod
    def get_url(self):
        pass


class HttpRequest(HttpRequestAbstract):
    def get(self, **kwargs):
        if self._url:
            self._response = self._request.get(self._url, headers=self._headers, **kwargs)
        else:
            raise Exception('Empty url!')
        return self

    def set_headers(self, headers):
        self._headers = headers
        return self

    def get_headers(self):
        return self._headers

    def get_last_request(self):
        pass

    def post(self, data=None, **kwargs):
        if self._url:
            self._response = self._request.post(self._url, data=json.dumps(data), headers=self._headers, **kwargs)
        else:
            raise Exception('Empty url!')
        return self

    def put(self, data=None, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def get_response_content(self):
        if self._response:
            return self._response.text
        else:
            return None

    def get_response_status(self):
        if self._response:
            return self._response.status_code
        else:
            return None

    def set_url(self, url):
        self._url = url
        return self

    def get_url(self):
        return self._url


class HttpRequestFactory:
    @staticmethod
    def create(req_type):
        if req_type == 'requests':
            return HttpRequest(requests)
        else:
            raise TypeError('Unknown Factory.')
