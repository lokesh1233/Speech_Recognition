# import scipy.io.wavfile as wav
import speech_recognition as sr     # import the library

import uuid
import urllib
import os
from config  import configuration
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SpeechToText():

    def __init__(self, modelType="speechRecog"):

        self.staudio = configuration.staudio
        self.modelType = modelType
        if modelType =="deepspeech":
            # deepspeech model
            import deepspeech
            self.ds = self.load_deepspeech_model()
        elif modelType == "speechwavenet":
            # speech to text wavenet model
            from wavenet import recognize
        else:
            # speech recognition model
            self.speechRecog = sr.Recognizer()


    def load_deepspeech_model(self):
        N_FEATURES = 25
        N_CONTEXT = 9
        BEAM_WIDTH = 500
        LM_ALPHA = 0.75
        LM_BETA = 1.85
        ds = deepspeech.Model('deepspeech_model/deepspeech-0.7.3-models.pbmm')
        return ds

    def output_fileCreate(self, text):
        sid = str(uuid.uuid4())
        received_file = self.staudio + 'output_' + sid + '.wav'
        urllib.request.urlretrieve(text, received_file)
        # path = os.path.dirname(__file__)
        # return "audio/output_{0}.wav".format(sid)
        return received_file
        # return wav.read("audio/output_{0}.wav".format(sid))

    def predictText(self, text):
        audioFile = self.output_fileCreate(text)
        logger.debug("TS file name" + audioFile)
        message = ""
        if self.modelType =="deepspeech":
            audio, fs = wav.read(audioFile)
            message = self.ds.stt(audio, fs)
        elif self.modelType == "speechwavenet":
            message = recognize.predict_wavenet(audioFile)
        else:
            message = self.predict_recognition(audioFile)
        return {"text": message}

    # speerch recognition prediction
    def predict_recognition(self, filename):
        # recognize the chunk
        with sr.AudioFile(filename) as source:
            # remove this if it is not working
            # correctly.
            self.speechRecog.adjust_for_ambient_noise(source)
            audio_listened = self.speechRecog.listen(source)
        try:
            # try converting it to text
            # rec = r.recognize_sphinx(audio_listened)
            rec = self.speechRecog.recognize_google(audio_listened)
            # write the output to the file.
            return rec

            # catch any errors.
        except sr.UnknownValueError:
            msg = "Could not understand audio"
            return msg

        except sr.RequestError as e:
            msg = "Could not request results. check your internet connection"
            return msg