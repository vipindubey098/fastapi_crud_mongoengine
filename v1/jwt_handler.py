# This file is responsible for signing, encoding, decoding and returning JWTs.
from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Header, Request, Path, Body
import time
import jwt
from decouple import config
from blogs_management import *

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Function returns the generated token (JWTs)
def token_response(token: str):
    return {
        "access_token" : token
    }


def signJWT(userID:str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    print(userID)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except CustomExceptionHandler as e:
        raise HTTPException(status_code=e.code, message=e.message)