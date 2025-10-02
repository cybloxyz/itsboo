import vosk
from vosk import KaldiRecognizer, Model
import sounddevice as sd
import queue
import json
import pyttsx3
import threading

responses = {
    "hi" : "yeah, hello what makes you talk to me?",
    "nothing" : "you better sleep!",
    "shut up" : "then what",
    "introduce" : "i am roboo i am nothing",
    "stupid" : "such you",
    "bye bye" : "good, go from my code"
    
}


tts_lock = threading.Lock()

spoken = set()

model = Model(r"./vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)

q = queue.Queue()

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)

def callback(indata, frames, time, status):
    """callback for sounddevice push audio to queue"""
    if status:
        print(status)
    q.put(bytes(indata))
    
def speak(reply_text):
    def run():
        with tts_lock:
            engine.say(reply_text)
            engine.runAndWait()
    threading.Thread(target=run).start()
    
try:
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("i am listening...ctrl + c to stop")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip().lower()
                if text not in spoken:
                    reply = responses.get(text, "i don't understand!!")
                    print("you said:", text)
                    speak(reply)
                    spoken.add(text)
                    
                    
            else:
                pass
            
except KeyboardInterrupt:
    print("\nstopped")
    