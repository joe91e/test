from flask_restful import Resource
from flask import request
LIMIT = "maxResult"
LIMIT_DEFAULT = 6
OFFSET = "start"
OFFSET_DEFAULT = 0


class BaseResource(Resource):
    api_request = request

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
