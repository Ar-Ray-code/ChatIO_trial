from io import BytesIO
import numpy as np
import soundfile as sf
import speech_recognition as sr
import whisper

class SpeechRecognizer:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)
        self.recognizer = sr.Recognizer()

    def recognize(self):
        with sr.Microphone(sample_rate=16000) as source:
            print("何か話してください")
            audio = self.recognizer.listen(source)

        print("音声処理中...")
        wav_bytes = audio.get_wav_data()
        wav_stream = BytesIO(wav_bytes)
        audio_array, sampling_rate = sf.read(wav_stream)
        audio_fp32 = audio_array.astype(np.float32)

        result = self.model.transcribe(audio_fp32, fp16=False)
        print("=====")
        print(result["text"])
        print("=====")
        return result["text"]

    def close(self):
        self.recognizer = None
        self.model = None
