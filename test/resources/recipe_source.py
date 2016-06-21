from flask import make_response, jsonify, Response
from resources.base import BaseResource
from handler.http_request_handler import HttpRequestFactory
from redis import StrictRedis, ConnectionPool
from handler.request_handler import RequestHandler
import json

redis_conn_pool = ConnectionPool(host='localhost', port=6379, db=0)
redis_cache = StrictRedis(connection_pool=redis_conn_pool)


class RecipeMetadata(BaseResource):
    def get(self, data_name):
        query_url = "{}".format(self.api_request.path)
        cache_value = redis_cache.get(query_url)
        if cache_value is not None and cache_value != "None":
            return make_response(jsonify(message="returning from cache"), 200)
        else:
            redis_cache.set(query_url, 1)
            return make_response(jsonify(message="caching [%s]" % query_url), 200)


class RecipeSearch(BaseResource):
    def get(self):
        query_url = "{}".format(self.api_request.path)
        query_string = self.api_request.query_string
        if query_string is not None and len(query_string):
            query_url = "{}?{}".format(query_url, query_string)

        req_obj = HttpRequestFactory.create('requests')
        url = "http://api.yummly.com/v1/api{}".format(query_url)
        headers = {
            'content-type': 'application/json',
            'X-Yummly-App-ID': '9cce27e7',
            'X-Yummly-App-Key': 'b13c741344519e5f89cb0edb7e8043f6'
        }
        req_handler = RequestHandler(req_obj, redis_cache)
        res_tuple = req_handler.get(url, headers)
        response = res_tuple[0]
        status_code = res_tuple[1]
        return Response(
            response=response,
            status=status_code,
            mimetype='application/json'
        )


class Recipe(BaseResource):
    def get(self, recipe_id):
        return Response(
            response=json.dumps({"recipe_id": recipe_id}),
            status=200,
            mimetype='application/json'
        )
