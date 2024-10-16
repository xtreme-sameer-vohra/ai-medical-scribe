import time
import threading
import numpy as np
import whisper
import sounddevice as sd
from queue import Queue
from rich.console import Console

console = Console()
stt = whisper.load_model("base.en")


def record_audio(stop_event, data_queue):
    """
    Captures audio data from the user's microphone and adds it to a queue for further processing.
    Args:
        stop_event (threading.Event): An event that, when set, signals the function to stop recording.
        data_queue (queue.Queue): A queue to which the recorded audio data will be added.
    Returns:
        None
    """
    def callback(indata, frames, time, status):
        if status:
            console.print(status)
        data_queue.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000, dtype="int16", channels=1, callback=callback
    ):
        while not stop_event.is_set():
            time.sleep(0.1)

def transcribe(stop_event, data_queue):
    """
    Transcribes the given audio data using the Whisper speech recognition model.
    Args:
        stop_event (threading.Event): An event that, when set, signals the function to stop recording.
        data_queue (queue.Queue): A queue to which the recorded audio data will be read from.
    Returns:
        str: The transcribed text.
    """
    while not stop_event.is_set():
        text = ""
        time.sleep(1)
        audio_data = b"".join(list(data_queue.queue))
        audio_np = (
            np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        )

        if audio_np.size > 0:
            with console.status("Transcribing..."):
                result = stt.transcribe(audio_np, fp16=False)  # Set fp16=True if using a GPU
                text = result["text"].strip()
            console.print(f"[yellow]You: {text}")

    console.print(f"[green]Recording Stopped")
    console.print(f"[green]Final transcript: {text}")


console.input(
    "Press Enter to start recording, then press Enter again to stop."
)

data_queue = Queue()  # type: ignore[var-annotated]
stop_event = threading.Event()
recording_thread = threading.Thread(
    target=record_audio,
    args=(stop_event, data_queue),
)
recording_thread.start()

transcribing_thread = threading.Thread(
    target=transcribe,
    args=(stop_event, data_queue),
)
transcribing_thread.start()

input()
stop_event.set()
recording_thread.join()
transcribing_thread.join()

console.print("[blue]Session ended.")