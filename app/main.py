import httpx

from fastapi import FastAPI, File, UploadFile


app = FastAPI()

MODEL_SERVER_URL = "https://2795-203-255-190-41.ngrok-free.app/predict"
INIT_BOUND = 0.3
MIN_BOUND = 0.04
MAX_BOUND = 0.1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/adt/init-bound")
def get_init_bound():
    return INIT_BOUND


@app.get("/adt/min-bound")
def get_init_bound():
    return MIN_BOUND


@app.get("/adt/max-bound")
def get_init_bound():
    return MAX_BOUND


@app.post("/adt")
def drum_transcription(file: UploadFile = File(...), bpm: int = 0):
    response = httpx.post(
        MODEL_SERVER_URL, files={"file": (file.filename, file.file)}, timeout=None
    )

    drum_data = response.json()
    drum_instrument = drum_data["drum_instrument"]
    onsets_arr = drum_data["onsets_arr"]

    result = []
    for drum in drum_instrument:
        idx = drum[0]
        pitch = drum[1]
        ts = onsets_arr[idx]
        for p in pitch:
            result.append({"pitch": p, "ts": ts})

    return {"result": result}
