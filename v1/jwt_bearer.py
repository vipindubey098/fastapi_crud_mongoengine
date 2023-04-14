# This function of this file is to check whether the request is authrorized or not [Verification of the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request: Request):
        credentails : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentails:
            if not credentails.scheme == "Bearer":
                raise HTTPException(status_code = 403, details="Invalud or Expired token!")
            return credentails.credentials
        else:
            raise HTTPException(status_code = 403, details="Invalud or Expired token!")


    def verify_jwt(self, jwtoken : str):
        isTokenvalid : bool = False  # A false flag
        payload = decodeJWT()
        if payload:
            isTokenvalid = True
        return isTokenvalid
