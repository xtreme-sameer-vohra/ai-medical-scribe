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
1. `ollama pull mistral`. This fetches the mistral llm

### Application
1. `python3.12 -m venv venv-ai-scribe`. This creates a virtual python environment. `venv-ai-scribe` will be the directory where python will install the dependencies.
1. `source venv-ai-scribe/bin/activate`. This activates the virtual environment on Mac OSX.
1. `pip install -r requirements.txt`. This installs the dependencies required
1. `streamlit run app.py`. Runs the application. The output contains a link to access the application (eg. http://localhost:8501) using a browser

## Configuration
`config.yaml` has the defaults used by the application. The application uses OpenAI Whisper `base.en` transcription model. Other options can be found in [Available Models and Sizes](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages). The application uses Mistral's `mistral` 7B LLM model. Other options can be found in [Ollama Model Library](https://ollama.com/library). The default prompt to the LLM generates a SOAP note and can be changed for different requirements or formats.

## Reference
- [Jarvis like assistant](https://medium.com/@vndee.huynh/build-your-own-voice-assistant-and-run-it-locally-whisper-ollama-bark-c80e6f815cba)
