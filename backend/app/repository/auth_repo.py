
from datetime import datetime, timedelta
from typing import Optional


from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose import ExpiredSignatureError, JWTError

from jose.exceptions import ExpiredSignatureError, JWSError, JWTClaimsError

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_YEARS, ACCESS_TOKEN_EXPIRE_TYPE


class JWTRepo:

    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def generate_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = self.data.copy()
        if expires_delta :
            expire = datetime.utcnow() + expires_delta
        elif ACCESS_TOKEN_EXPIRE_TYPE == "DAYS":
            expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            to_encode.update({"exp": expire})
        elif ACCESS_TOKEN_EXPIRE_TYPE == "YEARS":
            expire = datetime.utcnow() + timedelta(year=ACCESS_TOKEN_EXPIRE_YEARS)
            to_encode.update({"exp": expire})
        elif ACCESS_TOKEN_EXPIRE_TYPE == "MINUTES":
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
        else:
            to_encode.update()
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    def decode_token(self):
        try:
            decode_token = jwt.decode(
                self.token, SECRET_KEY, algorithms=[ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})

    @staticmethod
    def extract_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
           raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})

class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            return credentials.credentials
        
        else:
                raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})
        


    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            return True if jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM]) is not None else  False
        except ExpiredSignatureError:
           raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
        

class JWTBearerAdmin(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearerAdmin, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAdmin, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            try:
                if JWTRepo.extract_token(credentials.credentials)["role"] != "admin":
                    raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            except:
                raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
            return credentials.credentials
        else:
                raise HTTPException(
                status_code=403, detail={"status": "Forbidden", "message": "Invalid authorization code."})
        
    @staticmethod
    def verify_jwt(jwt_token: str):
        try:
            return True if jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM]) is not None else  False
        except ExpiredSignatureError:
           raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid token or expired token."})
        except JWTError:
            raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Invalid authentication schema."})