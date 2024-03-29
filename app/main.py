from app.rhythm_detection import RhythmDetection
import httpx

from typing import Union
from fastapi import FastAPI, File, UploadFile


app = FastAPI()

MODEL_SERVER_URL = "https://d595-203-255-190-41.ngrok-free.app/predict"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/adt")
def drum_transcription(file: UploadFile = File(...), bpm: int = 0):
    response = httpx.post(
        MODEL_SERVER_URL, files={"file": (file.filename, file.file)}, timeout=None
    )

    drum_data = response.json()
    print(drum_data)
    drum_instrument = drum_data["drum_instrument"]
    onsets_arr = drum_data["onsets_arr"]
    audio_total_sec = drum_data["audio_total_sec"]

    rhythm = RhythmDetection.get_rhythm(bpm, audio_total_sec, onsets_arr)

    result = []
    for drum in drum_instrument:
        idx = drum[0]
        pitch = drum[1]
        ts = rhythm[idx]
        result.append({"pitch": pitch, "ts": ts})

    return {"result": result}
