import traceback
import sys
import pprint
from werkzeug.exceptions import HTTPException, default_exceptions
from flask import Flask, session, make_response, jsonify
from flask_restful import Api
from handler.http_request_handler import HttpRequestFactory
from redis import StrictRedis, ConnectionPool

redis_conn_pool = ConnectionPool(host='localhost', port=6379, db=0)
redis_cache = StrictRedis(connection_pool=redis_conn_pool)
app = Flask(__name__)

"""
YUMMLY API USAGE

METADATA
http://api.yummly.com/v1/api/metadata/ingredient?_app_id=<id>&_app_key=<api_key>
http://api.yummly.com/v1/api/metadata/allergy?_app_id=<id>&_app_key=<api_key>
http://api.yummly.com/v1/api/metadata/diet?_app_id=<id>&_app_key=<api_key>
http://api.yummly.com/v1/api/metadata/cuisine?_app_id=<id>&_app_key=<api_key>
http://api.yummly.com/v1/api/metadata/course?_app_id=<id>&_app_key=<api_key>

SEARCH QUERY PARAMETERS:
q: <search phrase>
requirePictures: 'True'
allowedIngredient[]: <ingredient name>
    ->  recipes MUST contain this ingredient name. For e.g.
        if you enter beef as an ingredient, recipes returned MUST contain beef.
excludedIngredient[]: <ingredient name>
allowedAllergy[]: <allergy name>
allowedDiet[]: <diet name>
allowedCuisine[]: <cuisine name>
    ->  recipes MUST be one of these cuisine types. For e.g. if you specify
        '&allowedCuisine[]=korean&allowedCuisine[]=japanese' the results MUST
        contain korean and japense recipes
excludedCuisine[]: <cuisine name>
allowedCourse[]: <course name>
    ->  recipes must be of this course type: for e.g. main dish or dessert
excludedCourse[]: <course name>
allowedHoliday[]: <holiday name>
excludedHoliday[]: <holiday name>
maxTotalTimeInSeconds: <max prep + cook time in seconds>
nutrition.ATTR_NAME.{min|max}: &nutrition.FAT.max=20&nutrition.PROCNT.min=15
maxResult: <max result count>
start: <offset>
flavor.{sweet|meaty|sour|bitter|sweet|piquant}.{min|max}

"""

@app.route('/')
def hello_world():
    print(HttpRequestFactory)
    req_obj = HttpRequestFactory.create('requests')
    req_obj.set_headers(
        {
        'content-type': 'application/json',
        'X-Yummly-App-ID': '9cce27e7',
        'X-Yummly-App-Key': 'b13c741344519e5f89cb0edb7e8043f6'
        }
    )
    req_obj.set_url("http://api.yummly.com/v1/api/recipes?q=onion+soup")
    req_obj.get()
    res = req_obj.get_response_content()
    status_code = req_obj.get_response_status()
    return make_response(res, status_code)

@app.route('/metadata/<string:data_name>')
def get_metadata(data_name):
    url = '/metadata/' + data_name
    redis_value = redis_cache.get(url)
    if redis_value is not None:
        return make_response(jsonify(message="returning from cache"), 200)
    else:
        redis_cache.set(url, 1)
        return make_response(jsonify(message="caching [%s]" % url), 200)

@app.route('/search')
def search_recipes():
    return make_response(jsonify(message="hello"), 200)

@app.route('/recipe/<int:recipe_id>')
def get_recipe(recipe_id):
    return make_response(jsonify(recipe_id=recipe_id), 200)

if __name__ == '__main__':
     app.run(
      host='0.0.0.0',
      port=8000
     )
