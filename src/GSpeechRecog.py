import speech_recognition as sr     # import the library
r = sr.Recognizer()
# filename = '../audio/audio.wav'

def predict_recognition(filename):
    # recognize the chunk
    with sr.AudioFile(filename) as source:
        # remove this if it is not working
        # correctly.
        r.adjust_for_ambient_noise(source)
        audio_listened = r.listen(source)
    try:
        # try converting it to text
        # rec = r.recognize_sphinx(audio_listened)
        rec = r.recognize_google(audio_listened)
        # write the output to the file.
        print(rec)
        return rec

        # catch any errors.
    except sr.UnknownValueError:
        msg = "Could not understand audio"
        print(msg)
        return msg

    except sr.RequestError as e:
        msg = "Could not request results. check your internet connection"
        print(msg)
        return msg