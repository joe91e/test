import traceback
import sys
import pprint
from werkzeug.exceptions import HTTPException, default_exceptions
from flask import Flask, session, make_response, jsonify
from flask_restful import Api
from services import CFG_OBJ
from utils.logger import LoggerFactory
from resources.recipe_source import RecipeMetadata, RecipeSearch, Recipe
from datetime import datetime

app = Flask(__name__)
app.config.from_object(CFG_OBJ)
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

# register routes
api.add_resource(RecipeMetadata, '/metadata/<string:data_name>')
api.add_resource(RecipeSearch, '/recipes')
api.add_resource(Recipe, '/recipe/<string:recipe_id>')

# function to log all exceptions from python system traceback
def log_all_exceptions(logger):
    logger.log("\nException occurred at: {}".format(datetime.now()))
    exc_type, exc_value, exc_tb = sys.exc_info()
    error_list = traceback.format_exception(exc_type, exc_value, exc_tb)
    parsed_exceptions = parse_traceback(error_list)
    for exception in parsed_exceptions:
        logger.log(exception)

# parse the python system traceback so that we can print/log
def parse_traceback(traceback_list):
    parsed_output = []

    another_exception_msg = 'During handling of the above exception, another exception occurred:'
    new_exception_msg = 'Traceback (most recent call last):'
    exception_location = 'File "/'
    exception_separator = '-' * 80
    message_separator = '=' * 80

    cur_exception_info = ''

    for traceback_line in traceback_list:
        if another_exception_msg in traceback_line or new_exception_msg in traceback_line:
            if cur_exception_info != '':
                parsed_output.append(cur_exception_info)
                parsed_output.append(exception_separator)
                cur_exception_info = ''
        elif exception_location in traceback_line:
            cur_exception_info = traceback_line
        else:
            cur_exception_info += traceback_line

    if cur_exception_info != '':
        parsed_output.append(cur_exception_info)
        parsed_output.insert(0, message_separator)
        parsed_output.append(message_separator)

    return parsed_output

# catch ALL errors within the app. this is how we centralize error handling
@app.errorhandler(Exception)
def system_error_handler(sys_error):
    if isinstance(sys_error, HTTPException): #or isinstance(sys_error, APIError):
        message = sys_error.description
        status_code = sys_error.code
    else:
        message = str(sys_error)
        status_code = 500

    error_info = traceback.format_exc()
    log_all_exceptions(logger)

    # This should be skipped depending on config
    if(CFG_OBJ.get('DEBUG') == True):
        print(error_info)
    return make_response(jsonify(message=message), status_code)

for error in default_exceptions.items():
    app.error_handler_spec[None][error] = system_error_handler
    app.error_handler_spec[None][error[0]] = system_error_handler

if __name__ == '__main__':
    # setup logger
    log_type = CFG_OBJ.get('LOGGING.TYPE')
    log_path = CFG_OBJ.get('LOGGING.PATH')
    logger = LoggerFactory.create(log_type, log_path)

    # log the app start message with a timestamp
    separator = '*' * 80
    logger.log("\n" + separator)
    logger.log("Application Starting :: {}".format(datetime.now()))
    logger.log("\n" + separator)

    # run the app
    app.run(**CFG_OBJ.FLASK_RUN_OPTS)
