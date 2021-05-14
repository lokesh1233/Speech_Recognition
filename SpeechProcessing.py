from flask import jsonify, abort, render_template, send_from_directory
# request, Blueprint,
import json
from sanic import Blueprint, response
from sanic.response import html
from jinja2 import Environment, PackageLoader

# env = Environment(loader=PackageLoader('SpeechProcessing', 'templates'))

# from flask_socketio import SocketIO
REQUEST_API = Blueprint('request_api', __name__)


from config import configuration as cnfg
from Exception.InvalidUsage import InvalidUsage
from src.SpeechToText import SpeechToText
from src.TextToSpeech import TextToSpeech
from socketProcessing import SocketIOInput



ST = SpeechToText()
TS = TextToSpeech()


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

def speechToTextFun(message):
    return ST.predictText(message)

def textToSpeechFun(message):
    return TS.send_text_message(message)

socketio = SocketIOInput(speechToTextFun, textToSpeechFun)
def get_sockets():
    return socketio.blueprint()



@REQUEST_API.route('/', methods=['GET'])
async def root(request):
    # template = env.get_template('VUE.html')
    # html_content = template.render()
    # return html(html_content)
    return await response.file('templates/VUE.html')

@REQUEST_API.route('/js/<path:path>', methods=['GET'])
async def send_js(request, path):
    return await response.file('templates/js/'+ path)

## generate Template and return url
@REQUEST_API.route('/SpeechToText', methods=['POST'])
def generateTemplate(request):
    if request.method == 'POST':
        # check if the post request has the file part
        # return json.dumps(speechToTextFun(request.get_json(force=True)['blobData']))
        return response.json(speechToTextFun(request.json['blobData']))
        # return "Speech to Text"

## generate Template and return url
@REQUEST_API.route('/TextToSpeech', methods=['POST'])
def resumeTemplate(request):
    if request.method == 'POST':
        # check if the post request has the file part
        # return json.dumps(textToSpeechFun(request.get_json(force=True)['message']))
        return response.json(textToSpeechFun(request.json['message']))
        # return "Text To Speech"
        # return send_from_directory(cnfg.GENERATEDDOCS, employee_code, as_attachment=True)




# @REQUEST_API.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response

