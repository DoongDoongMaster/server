import os
import httpx

from fastapi import APIRouter, File, UploadFile, HTTPException


router = APIRouter(
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)

INIT_BOUND = 0.3
MIN_BOUND = 0.1
MAX_BOUND = 0.15


@router.get("/adt/init-bound")
def get_init_bound():
    return INIT_BOUND


@router.get("/adt/min-bound")
def get_min_bound():
    return MIN_BOUND


@router.get("/adt/max-bound")
def get_max_bound():
    return MAX_BOUND


@router.post("/adt/predict")
def drum_transcription(file: UploadFile = File(...)):
    try:
        response = httpx.post(
            os.environ["MODEL_SERVER_URL"],
            files={"file": (file.filename, file.file)},
            timeout=None,
        )
    except:
        raise HTTPException(status_code=503, detail="Model server error")

    try:
        drum_data = response.json()
        drum_instrument = drum_data["drum_instrument"]
        onsets_arr = drum_data["onsets_arr"]
    except:
        raise HTTPException(status_code=404, detail="Not Found")

    result = []
    for drum in drum_instrument:
        idx = drum[0]
        pitch = drum[1]
        ts = onsets_arr[idx]
        for p in pitch:
            result.append({"pitch": p, "ts": ts})

    return {"result": result}
