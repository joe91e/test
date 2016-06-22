from flask_restful import Resource
from flask import request
from handler.http_request_handler import HttpRequestFactory
from redis import StrictRedis, ConnectionPool
from handler.request_handler import RequestHandler
import json

redis_conn_pool = ConnectionPool(host='localhost', port=6379, db=0)
redis_cache = StrictRedis(connection_pool=redis_conn_pool)

LIMIT = "maxResult"
LIMIT_DEFAULT = 6
OFFSET = "start"
OFFSET_DEFAULT = 0


class BaseResource(Resource):
    api_request = request
    req_obj = HttpRequestFactory.create('requests')
    headers = {
        'content-type': 'application/json',
        'X-Yummly-App-ID': '9cce27e7',
        'X-Yummly-App-Key': 'b13c741344519e5f89cb0edb7e8043f6'
    }
    req_obj.set_headers(headers)
    req_handler = RequestHandler(req_obj, redis_cache)


    def __init__(self):
        super(BaseResource, self).__init__()

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
