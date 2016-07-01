from flask_restful import Resource
from flask import request
from handler.http_request_handler import HttpRequestFactory
from redis import StrictRedis, ConnectionPool
from handler.request_handler import RequestHandler
from handler.storage_handler import RedisAdapter
import json
from services import CFG_OBJ


class BaseResource(Resource):

    def __init__(self):
        super(BaseResource, self).__init__()
        self.api_request = request
        self.req_obj = HttpRequestFactory.create('requests')
        self.req_obj.set_headers(CFG_OBJ.get('HEADERS'))
        redis_adapter = RedisAdapter()
        self.redis_cache = redis_adapter.get_instance()
        self.req_handler = RequestHandler(self.req_obj, self.redis_cache)

    def get_request_limit(self):
        limit = None
        if constants.LIMIT in self.api_request.args:
            limit = int(self.api_request.args.get(constants.LIMIT))
        if limit is None or limit > constants.LIMIT_DEFAULT:
            limit = constants.LIMIT_DEFAULT
        return limit

    def get_request_offset(self):
        offset = None
        if constants.OFFSET in self.api_request.args:
            offset = int(self.api_request.args.get(constants.OFFSET))
        if offset is None or offset < constants.OFFSET_DEFAULT:
            offset = constants.OFFSET_DEFAULT
        return offset

    def get_request_json_data(self):
        return self.api_request.get_json()
