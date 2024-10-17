import streamlit as st
import whisper
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample

audio_value = st.experimental_audio_input("Record note to transcribe")

stt = whisper.load_model("base.en")

if audio_value:
    st.audio(audio_value)
    print("reading binary data")
    sample_rate, audio_data = wavfile.read(audio_value)
    print("resampling audio")
    new_sample_rate = 16000  # For example, 16 kHz
    # Calculate the number of samples in the resampled audio
    num_samples = int(len(audio_data) * new_sample_rate / sample_rate)
    # Resample the audio data
    resampled_audio_data = resample(audio_data, num_samples)
    audio_np = resampled_audio_data.astype(np.float32) / 32768.0  # Assuming 16-bit PCM
    print("transcribing audio to text")
    result = stt.transcribe(audio_np, fp16=False)
    text = result["text"].strip()
    print("transcription complete :", text )
    st.write(text)