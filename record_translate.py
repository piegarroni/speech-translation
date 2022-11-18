import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.io.wavfile import write, read
import whisper
from transformers import WhisperProcessor, WhisperForConditionalGeneration

print(sd.query_devices(device=None, kind=None))

def record():
    """
    Method to record the audio signal from the computer's microphone
    """

    Fs = 8000  # Sampling frequency
    duration = 7 # Recording duration in seconds

    recording = sd.rec(frames=duration * Fs, samplerate=Fs, channels=1)  # Capture the voice

    print('start')
    sd.wait()
    print('end')

    # save file
    filename = str(os.getcwd()) + "\\speech-translation\\recording\\audio.wav"
    write(filename= filename, rate = Fs, data=recording)

    return filename



def plot_audio(filename):
    """
    Method to plot the audio signal recorded 
    """
    a = read(filename)
    recording = np.array(a[1],dtype=float)
    # plot audio file
    time = np.linspace(0, len(recording - 1) / 8000, len(recording - 1))
    print(recording)  
    plt.plot(time, recording)  
    plt.title("Voice Signal")
    plt.xlabel("Time [seconds]")
    plt.ylabel("Voice amplitude")
    plt.show()


def transcribe(filename):
    #filename = filename.split("\\")[-2] + "\\" + filename.split("\\")[-1]
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]


def translate(filename):
    """
    Translate from french (french speech to english transcrption)
    """

    # load model and processor
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")

    # load dummy dataset and read soundfiles
    #ds = load_dataset("common_voice", "fr", split="test", streaming=True)
    #ds = ds.cast_column("audio", Audio(sampling_rate=16_000))
    #input_speech = next(iter(ds))["audio"]["array"]

    # tokenize
    input_features = processor(filename, return_tensors="pt").input_features 
    forced_decoder_ids = processor.get_decoder_prompt_ids(language = "fr", task = "translate")

    predicted_ids = model.generate(input_features, forced_decoder_ids = forced_decoder_ids)
    translation = processor.batch_decode(predicted_ids, skip_special_tokens = True)
    print(translation)



def detect_language(filename):
    """
    detect language to then pass variable to translate()
    """

    model = whisper.load_model("base")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    language = {max(probs, key=probs.get)}

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)
    return language


file = record()
transcription = transcribe(file)
print("transcription: " + transcription)


print()
#print('translation:' + translate(file))
print()

language = detect_language(file)
print("Detected language: " + str(language[0]))