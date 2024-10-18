import streamlit as st
import whisper
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import requests

st.title("Medical AI Scribe")

audio_value = st.experimental_audio_input("Record note to transcribe")

stt = whisper.load_model("base.en")

prompt = "Write the following transcribed text into SOAP(Subjective, Objective, Assessment, and Plan) format. Use full sentences rather than bullet points under each section. Transcribed text:"

if 'transcribedtext' not in st.session_state:
    st.session_state.transcribedtext = ''

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
    st.session_state.transcribedtext = text

if 'transcribedtext' in st.session_state and len(st.session_state.transcribedtext) > 0:
    txt = st.text_area("Transcribed Text:", st.session_state.transcribedtext)
    print("Generating SOAP Note" )
    st.write("Generating SOAP Note")
    # Send the transcribed text to Ollama LLM
    api_endpoint = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mistral",
        "prompt": prompt + " " + text,
        "stream": False,
    }

    response = requests.post(api_endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        print("LLM response:", response_data)
        st.write(response_data['response'])
    else:
        print("Failed to get response from LLM:", response.status_code)
        st.write("Failed to get response from LLM:", response.status_code)