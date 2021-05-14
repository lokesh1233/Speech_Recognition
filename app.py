import argparse
import os
from flask import Flask, jsonify, make_response
from sanic import Sanic
from sanic_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import SpeechProcessing
from config import configuration as cnfg
from Exception.InvalidUsage import InvalidUsage
# from flask_socketio import SocketIO

APP = Sanic(__name__)

### swagger specific ###
SWAGGER_URL = '/api'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Resume Builder App"
    }
)
# APP.blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

APP.blueprint(SpeechProcessing.get_sockets(), url_prefix="/socket")
APP.blueprint(SpeechProcessing.get_blueprint(), url_prefix="/rest")


# @APP.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     # response = jsonify(error.to_dict())
#     response = error.message
#     status_code = error.status_code
#     return {'message':response}, status_code


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Resume Builder API")
    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()
    PORT = int(os.environ.get('PORT', 5000))
    CORS = CORS(APP)
    # socketio = SpeechProcessing.get_socket().register(APP)
    APP.run( host='0.0.0.0', port=cnfg.port, debug=ARGS.debug)
