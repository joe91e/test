import traceback
import sys
import pprint
from werkzeug.exceptions import HTTPException, default_exceptions
from flask import Flask, session, make_response, jsonify
from flask_restful import Api
#from handler.http_request_handler import HttpRequestFactory
#from redis import StrictRedis, ConnectionPool
#from handler.request_handler import RequestHandler
from resources.recipe_source import RecipeMetadata, RecipeSearch, Recipe

#redis_conn_pool = ConnectionPool(host='localhost', port=6379, db=0)
#redis_cache = StrictRedis(connection_pool=redis_conn_pool)
app = Flask(__name__)
api = Api(app)

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

api.add_resource(RecipeMetadata, '/metadata/<string:data_name>')
api.add_resource(RecipeSearch, '/recipes')
api.add_resource(Recipe, '/recipe/<string:recipe_id>')

"""
@app.errorhandler(Exception)
def system_error_handler(sys_error):
    if isinstance(sys_error, HTTPException) or isinstance(sys_error, APIError):
        message = sys_error.description
        status_code = sys_error.code
    else:
        message = str(sys_error)
        status_code = 500

    error_info = traceback.format_exc()
    # log_all_exceptions()

    # This should be skipped depending on config
    print(error_info)
    return make_response(jsonify(message=message), status_code)

for error in default_exceptions.items():
    app.error_handler_spec[None][error] = system_error_handler
    app.error_handler_spec[None][error[0]] = system_error_handler
"""

if __name__ == '__main__':
     app.run(
      host='0.0.0.0',
      port=8000
     )
