import speech_recognition as sr

def get_voice_input():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        return r.recognize_google(audio)
    except:
        return None
