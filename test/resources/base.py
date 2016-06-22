from flask_restful import Resource
from flask import request
from handler.http_request_handler import HttpRequestFactory
from redis import StrictRedis, ConnectionPool
from handler.request_handler import RequestHandler
from handler.storage_handler import RedisAdapter
import json

"""
@ick: move these four constants into constants/__init__.py
add `import constants` at the top.
access constants by constants.CONSTANT_NAME.
Replace constants being used in the BaseResource class
from `CONSTANT_NAME` -> to `constants.CONSTANT_NAME`
and then remove these below four lines once they are no longer being
referenced (no longer needed).
"""
LIMIT = "maxResult"
LIMIT_DEFAULT = 6
OFFSET = "start"
OFFSET_DEFAULT = 0


class BaseResource(Resource):

    def __init__(self):
        super(BaseResource, self).__init__()
        self.api_request = request
        self.req_obj = HttpRequestFactory.create('requests')
        """
        @ick: try moving these headers to the config file!
        """
        headers = {
            'content-type': 'application/json',
            'X-Yummly-App-ID': '9cce27e7',
            'X-Yummly-App-Key': 'b13c741344519e5f89cb0edb7e8043f6'
        }
        self.req_obj.set_headers(headers)
        redis_adapter = RedisAdapter()
        self.redis_cache = redis_adapter.get_instance()
        self.req_handler = RequestHandler(self.req_obj, self.redis_cache)

    def get_request_limit(self):
        limit = None
        if LIMIT in self.api_request.args:
            limit = int(self.api_request.args.get(LIMIT))
        if limit is None or limit > LIMIT_DEFAULT:
            limit = LIMIT_DEFAULT
        return limit

    def get_request_offset(self):
        offset = None
        if OFFSET in self.api_request.args:
            offset = int(self.api_request.args.get(OFFSET))
        if offset is None or offset < OFFSET_DEFAULT:
            offset = OFFSET_DEFAULT
        return offset

    def get_request_json_data(self):
        return self.api_request.get_json()
