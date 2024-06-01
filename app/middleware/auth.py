import firebase_admin
from firebase_admin import auth
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class FirebaseTokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith('/models'):
            return await call_next(request)

        token = request.headers.get("Authorization")

        if token:
            try:
                token = token.split(" ")[1]  # "Bearer <token>" 형태일 경우
                decoded_token = auth.verify_id_token(token)
                request.state.user = decoded_token  # 사용자 정보를 request.state에 저장
            except Exception as e:
                return JSONResponse(status_code=403, content="Invalid token")
        else:
            return JSONResponse(status_code=403, content="Token required")

        response = await call_next(request)
        return response

