from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests

from dotenv import load_dotenv
import os
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure AD Configuration
TENANT_ID = os.getenv("TENANT_ID")
API_ID = os.getenv("API_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
JWKS_URL = f"{AUTHORITY}/discovery/v2.0/keys"
AUDIENCE = f"api://{API_ID}"

print( TENANT_ID )
print( API_ID )


# Token validation
security = HTTPBearer()


def get_jwk():
    response = requests.get(JWKS_URL)
    response.raise_for_status()
    return response.json()


def decode_jwt(token: str):
    jwks = get_jwk()
    unverified_header = jwt.get_unverified_header(token)
    key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
    if not key:
        raise HTTPException(status_code=401, detail="Invalid token header")
    return jwt.decode(token, key, algorithms=["RS256"], audience=AUDIENCE)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401, detail=f"Token validation failed: {str(e)}"
        )


def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        roles = user.get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=403, detail="Access forbidden: insufficient role"
            )
        return user

    return role_checker


# Routes
@app.get("/")
def public():
    return {"message": "Public endpoint"}


@app.get("/admin")
def user_route(user=Depends(require_role("app.all"))):
    return {"message": f"Hello Admin: {user.get('name')}"}


@app.get("/pii")
def admin_route(user=Depends(require_role("app.pii"))):
    return {"message": f"Hello pii data : {user.get('name')}"}


@app.get("/user")
def admin_route(user=Depends(require_role("app.access"))):
    return {"message": f"Hello access provide to : {user.get('name')}"}
