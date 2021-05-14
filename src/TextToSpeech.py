# import scipy.io.wavfile as wav
import time
from typing import Optional, Text, Any, List, Dict, Iterable
import json
import uuid
from gtts import gTTS
# import pyttsx3
from config import configuration
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class TextToSpeech():
    def __init__(self, modelType="speechRecog"):
        self.tsaudio = configuration.tsaudio
        self.modelType = modelType
        if modelType == "tts":
            # tts model
            # from src import TTSModel
            pass
        elif modelType == "ttsx3":
            # ttsx3 model
            self.ttsx3engine = pyttsx3.init()
        else:
            # speech recognition model
            # modelType = "speechRecog"
            pass



    def _send_audio_message(self, socket_id, response, **kwargs: Any):
         # type: (Text, Any) -> None
        """Sends a message to the recipient using the bot event."""

        ts = time.time()
        OUT_FILE = str(ts) + '.wav'
        link = "http://localhost:8888/" + OUT_FILE
        wav_norm = self.tts_predict(self.MODEL_PATH, response['text'], self.CONFIG, self.use_cuda, OUT_FILE)

        return json.dumps({'text': response['text'], "link": link})

        # await self.sio.emit(self.bot_message_evt, {'text': response['text'], "link": link}, room=socket_id)

    def send_text_message(self, message=""):
        """Send a message through this channel."""
        if message == "":
            return {"text":"No text is defined to create audio file"}
        sid = str(uuid.uuid4())
        addFile = 'output_' + sid + '.wav'
        audioFilePath = self.tsaudio + addFile

        if self.modelType == "tts":
            # tts model
            # from src import TTSModel
            pass
        elif self.modelType == "ttsx3":
            # ttsx3 model
            audioFile = self.pyttsx3_fun(message, audioFilePath)
        else:
            audioFile =  self.gTextToSpeech(message, audioFilePath)

        logger.debug("TS file name" + addFile)

        return {'text': message, "link": configuration.audioFilePath+addFile}
        # return self._send_audio_message(self.sid, {"text": message})

    # google textToSpeech
    def gTextToSpeech(self, text, addFile):
        tts = gTTS(text, lang='en')
        tts.save(addFile)
        return addFile


    def pyttsx3_fun(self, text, audioFile):
        self.ttsx3engine.save_to_file(text, audioFile)
        self.ttsx3engine.runAndWait()
        return audioFile
        # engine.runAndWait()