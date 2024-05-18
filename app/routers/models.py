import os
import io
import logging
import requests
import xml.etree.ElementTree as ET

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
def drum_transcription(file: bytes = File(...)):
    logging.info("post request enter")
    try:
        logging.info("I'm waiting respond for model server ...")
        response = requests.post(os.environ["MODEL_SERVER_URL"], files={"file": (file)})
        logging.info("model server done !!!")
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


@router.post("/omr/predict")
def drum_transcription(file: bytes = File(...)):
    dummy_file = "app/static/dummy.xml"

    # XML 데이터를 파싱하여 ElementTree 객체로 변환
    tree = ET.parse(dummy_file)

    # BytesIO 객체를 사용하여 XML 트리를 바이트 데이터로 변환
    byte_io = io.BytesIO()
    tree.write(byte_io, encoding="utf-8", xml_declaration=True)

    # 바이트 데이터를 가져옴
    byte_data = byte_io.getvalue()

    return {"result": byte_data}
