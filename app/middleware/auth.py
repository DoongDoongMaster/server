from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette.requests import Request
from firebase_admin import auth
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

class AuthRequired(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthRequired, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(status_code=401, detail="Token Required")

        token_type, token = auth_header.split(" ")

        if token_type != "Bearer":
            raise HTTPException(status_code=402, detail="Invalid Token")

        try:
            logger.debug(token)
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token
            logger.debug(decoded_token)
        except Exception as e:
            raise HTTPException(status_code=403, detail="Invalid Token")