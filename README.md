# AI Medical Scribe
This is a WIP project.
It is a AI based scribe that generates a SOAP note of the patient's visit. It uses OpenAI's whisper for transcribing audio to text. It uses mistral to generate a SOAP note from the transcribed text. The transcription and soap note generation are done locally.

## Pre-requisites
- [Python](https://www.python.org/downloads/release/python-3120/) (tested with 3.12)
- [Ollama](https://ollama.com/)

### Pre-requisites using brew
If you're familiar with [brew](https://brew.sh/), use the following links
- [Python](https://formulae.brew.sh/formula/python@3.12#default)
- [Ollama](https://formulae.brew.sh/formula/ollama#default)

## Setup
### Ollama
- Pull mistral llm `ollama pull mistral`

### Application
- Create a python virtual env `python3.12 -m venv venv-ai-scribe`. `venv-ai-scribe` will be the directory where python will install the dependencies in the next step
- Activate the virtual environment. On Mac OSX, `source venv-ai-scribe/bin/activate`
- Install the dependencies, `pip install -r requirements.txt`
- Run the application `streamlit run ui-streamlit.py`

## TODO
- cache whisper model
- make llm model configurable
- make prompt configurable
- set temperature to 0
- auto generate soap note & remove button
- make whisper model configurable

## Isues
- Doesn't work with Python 3.13

## Reference
- [Jarvis like assistant](https://medium.com/@vndee.huynh/build-your-own-voice-assistant-and-run-it-locally-whisper-ollama-bark-c80e6f815cba)
