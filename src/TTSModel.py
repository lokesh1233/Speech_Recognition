import scipy.io.wavfile as wav
import time
from typing import Optional, Text, Any, List, Dict, Iterable
import json
import uuid
from config import configuration

import torch
from TTS.models.tacotron import Tacotron
from TTS.layers import *
from TTS.utils.data import *
from TTS.utils.audio import AudioProcessor
from TTS.utils.generic_utils import load_config
from TTS.utils.text import text_to_sequence
from TTS.utils.synthesis import synthesis
from utils.text.symbols import symbols, phonemes
from TTS.utils.visual import visualize


import logging
logger = logging.getLogger(__name__)

class TextToSpeech():
    def __init__(self):
        self.model, self.ap, self.MODEL_PATH, self.CONFIG, self.use_cuda  = self.load_tts_model()


    def load_tts_model(self):

        MODEL_PATH = 'tts_model/best_model.pth.tar'
        CONFIG_PATH = 'tts_model/config.json'
        CONFIG = load_config(CONFIG_PATH)
        use_cuda = False

        num_chars = len(phonemes) if CONFIG.use_phonemes else len(symbols)
        model = Tacotron(num_chars, CONFIG.embedding_size, CONFIG.audio['num_freq'], CONFIG.audio['num_mels'], CONFIG.r,
                         attn_windowing=False)

        num_chars = len(phonemes) if CONFIG.use_phonemes else len(symbols)
        model = Tacotron(num_chars, CONFIG.embedding_size, CONFIG.audio['num_freq'], CONFIG.audio['num_mels'], CONFIG.r,
                         attn_windowing=False)

        # load the audio processor
        # CONFIG.audio["power"] = 1.3
        CONFIG.audio["preemphasis"] = 0.97
        ap = AudioProcessor(**CONFIG.audio)

        # load model state
        if use_cuda:
            cp = torch.load(MODEL_PATH)
        else:
            cp = torch.load(MODEL_PATH, map_location=lambda storage, loc: storage)

        # load the model
        model.load_state_dict(cp['model'])
        if use_cuda:
            model.cuda()

        # model.eval()
        model.decoder.max_decoder_steps = 1000
        return model, ap, MODEL_PATH, CONFIG, use_cuda

    def tts(self, model, text, CONFIG, use_cuda, ap, OUT_FILE):
        import numpy as np
        waveform, alignment, spectrogram, mel_spectrogram, stop_tokens = synthesis(model, text, CONFIG, use_cuda, ap)
        ap.save_wav(waveform, OUT_FILE)
        wav_norm = waveform * (32767 / max(0.01, np.max(np.abs(waveform))))
        return alignment, spectrogram, stop_tokens, wav_norm

    def tts_predict(self, MODEL_PATH, sentence, CONFIG, use_cuda, OUT_FILE):

        align, spec, stop_tokens, wav_norm = self.tts(self.model, sentence, CONFIG, use_cuda, self.ap, OUT_FILE)
        return wav_norm

    def _send_audio_message(self, response):
         # type: (Text, Any) -> None
        """Sends a message to the recipient using the bot event."""

        ts = time.time()
        OUT_FILE = str(ts) + '.wav'
        link = "http://localhost:8888/" + OUT_FILE
        wav_norm = self.tts_predict(self.MODEL_PATH, response['text'], self.CONFIG, self.use_cuda, OUT_FILE)

        return json.dumps({'text': response['text'], "link": link})

        # await self.sio.emit(self.bot_message_evt, {'text': response['text'], "link": link}, room=socket_id)

    def send_text_message(self, message="", type="google"):
        """Send a message through this channel."""
        if message == "":
            return {"text":""}

        return self._send_audio_message({"text": message})