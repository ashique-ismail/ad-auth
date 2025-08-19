from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import httpx

import os

app = FastAPI()
bearer_scheme = HTTPBearer()

TENANT_ID = os.getenv("TENANT_ID")
API_ID = os.getenv("API_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
JWKS_URL = f"{AUTHORITY}/discovery/v2.0/keys"
AUDIENCE = f"api://{API_ID}"

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    async with httpx.AsyncClient() as client:
        jwks = (await client.get(JWKS_URL)).json()
    unverified_header = jwt.get_unverified_header(token)
    key = next(k for k in jwks["keys"] if k["kid"] == unverified_header["kid"])
    try:
        payload = jwt.decode(token, key, algorithms=["RS256"], audience=AUDIENCE)
        return payload
    except Exception as e:
        print( e )
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    return {"message": "Access granted", "user": user}
