from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import decode, PyJWTError

from auth.token import security, SECRET_KEY


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        email = payload.get('email')
        if not email:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {'email': email}
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
