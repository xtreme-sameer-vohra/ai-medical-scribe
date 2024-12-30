import streamlit as st
import whisper
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import requests
import yaml

@st.cache_resource
def load_config(file_name="config.yaml"):
    with open(file_name, 'r') as file:
        return yaml.safe_load(file)
config = load_config()

prompt = config['llm_prompt']

@st.cache_resource
def whisper_stt(model_name):
     return whisper.load_model(model_name)

def transcribe_audio(file):
    print("reading binary data")
    sample_rate, audio_data = wavfile.read(file)
    print("resampling audio")
    new_sample_rate = 16000  # 16 kHz
    # Calculate the number of samples in the resampled audio
    num_samples = int(len(audio_data) * new_sample_rate / sample_rate)
    # Resample the audio data
    resampled_audio_data = resample(audio_data, num_samples)
    audio_np = resampled_audio_data.astype(np.float32) / 32768.0  # Assuming 16-bit PCM
    print("transcribing audio to text")
    result = stt.transcribe(audio_np, fp16=False)
    text = result["text"].strip()
    return text

def query_llm(prompt, text):
    api_endpoint = config["llm_generate_url"]
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": config["llm_model"],
        "prompt": prompt + " " + text,
        "stream": False,
    }
    response = requests.post(api_endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        print("LLM response:", response_data)
        return response_data['response']
    else:
        print("Failed to get response from LLM:", response.status_code)
        return "Failed to get response from LLM:", response.status_code

st.title("Medical AI Scribe")
with st.spinner('Loading Text to voice model...'):
    stt = whisper_stt(config["transcription_model"])

audio_value = st.audio_input("Record note to transcribe")

if 'transcribedtext' not in st.session_state:
    st.session_state.transcribedtext = ''

if audio_value:
    st.audio(audio_value)
    with st.spinner('Transcribing...'):
        text = transcribe_audio(audio_value)
        print("transcription complete :", text )
        st.session_state.transcribedtext = text

if 'transcribedtext' in st.session_state and len(st.session_state.transcribedtext) > 0:
    txt = st.text_area("Transcribed Text:", st.session_state.transcribedtext)
    print("Generating SOAP Note" )
    st.subheader("SOAP Note", divider=True)
    with st.spinner('Generating...'):
        soap_note = query_llm(prompt, txt)
        st.write(soap_note)