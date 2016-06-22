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
        # parse url
        query_url = "{}".format(self.api_request.path)
        url = "http://api.yummly.com/v1/api{}".format(query_url)

        # make request
        res_tuple = self.req_handler.get(url)
        response_text = res_tuple[0]
        status_code = res_tuple[1]

        try:
            response_text = json.loads(response_text)
        except ValueError:
            pass

        response = {
            "data": response_text
        }
        print(response)
        return Response(
            response=json.dumps(response),
            status=status_code,
            mimetype='application/json'
        )


class RecipeSearch(BaseResource):
    def get(self):
        """
        @ICK: refactor this function like the RecipeMetadata:get func above.
        because the req_handler already exists in the BaseResource,
        it can be accessed by calling self.req_handler.
        There is no need to re-setup req_obj, headers
        """

        # parse url
        query_url = "{}".format(self.api_request.path)
        query_string = self.api_request.query_string
        if query_string is not None and len(query_string):
            query_url = "{}?{}".format(query_url, query_string)
        url = "http://api.yummly.com/v1/api{}".format(query_url)

        # setup and make request
        req_obj = HttpRequestFactory.create('requests')
        headers = {
            'content-type': 'application/json',
            'X-Yummly-App-ID': '9cce27e7',
            'X-Yummly-App-Key': 'b13c741344519e5f89cb0edb7e8043f6'
        }
        req_handler = RequestHandler(req_obj, redis_cache)
        res_tuple = req_handler.get(url, headers)

        # parse and return response
        response_text = res_tuple[0]
        response = {
            "data": json.loads(response_text)
        }
        status_code = res_tuple[1]
        return Response(
            response=json.dumps(response),
            status=status_code,
            mimetype='application/json'
        )


class Recipe(BaseResource):
    def get(self, recipe_id):
        # @ICK:
        # hit http://api.yummly.com/v1/api/recipe/<recipe_id>
        # where <recipe_id> will be replaced by the recipe_id passed in
        # as an argument

        # parse url
        """
        @ICK: your parse url code here
        """

        # setup and make request
        """
        @ICK: your setup and make request here
        """

        # parse and return reseponse
        """
        @ICK: your parse and return response here!
        in the end, the response should look like
        {
            "data": <JSON returned from api.yummly.com>
        }
        """
        response = {}

        return Response(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
