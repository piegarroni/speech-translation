import sounddevice as sd
import numpy as np
import whisper
from queue import Queue
import threading

# add thread for summarization, translation and frontend
# use speechrecognition library

class RecordingService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments
        self.duration =  5 #10
        self.Fs = 16000 #44100

    def run(self):
        while True:
            recording = sd.rec(frames=self.duration * self.Fs, samplerate=self.Fs, channels=1)  # Capture the voice
            print('recording started')
            sd.wait()
            print('recording stopped')

            recording = recording.flatten().astype(np.float32)
            self.audio_segments.put(recording)
            

class TranscriptionService(threading.Thread):
    def __init__(self, audio_segments: Queue):
        threading.Thread.__init__(self)
        self.audio_segments = audio_segments
        self.model = whisper.load_model("small.en")

    def run(self):
        while True:
            result = self.audio_segments.get()
            result = self.model.transcribe(result, fp16=False, language='English')

            print("result:")
            print(result.get("text"))
            self.audio_segments.task_done()


audio_segments = Queue()
recorder = RecordingService(audio_segments)
transcriber = TranscriptionService(audio_segments)

recorder.start()
transcriber.start()
