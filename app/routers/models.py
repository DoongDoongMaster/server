import os
import logging
import requests

from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from ..middleware import auth

router = APIRouter(
    prefix="/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
    dependencies=[
        Depends(
            auth.AuthRequired(),
        ),
    ],
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
def automatic_drum_transcription(file: bytes = File(...)):
    logging.info("post request enter")
    try:
        logging.info("I'm waiting respond for model server ...")
        response = requests.post(
            f'{os.environ["MODEL_SERVER_URL"]}/adt/predict', files={"file": (file)}
        )
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
def optical_music_recognition(file: UploadFile = File(...)):
    try:
        logging.info("[OMR] Received file upload")

        # 파일 내용을 읽어서 모델 서버로 전송
        file_content = file.file.read()

        # 파일을 모델 서버로 전송
        with requests.Session() as session:
            response = session.post(
                f'{os.environ["MODEL_SERVER_URL"]}/omr/predict',
                files={"file": (file.filename, file_content, file.content_type)},
            )

            # 응답 처리
            if response.status_code == 200:
                logging.info("Received response from model server")
                response_data = response.json()
                return response_data
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Not Found")
            else:
                raise HTTPException(status_code=503, detail="Model server error")

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
