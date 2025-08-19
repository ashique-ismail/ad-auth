# uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = [os.getenv("SCOPE")]

msal_app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

@app.get("/")
def home():
    return HTMLResponse('<a href="/login">Login with Microsoft</a>')

@app.get("/login")
def login():
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return RedirectResponse(auth_url)

@app.get("/auth/redirect")
def auth_redirect(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No authorization code found in the request."}

    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )

    if "access_token" in result:
        return {
            "access_token": result["access_token"],
            "id_token_claims": result.get("id_token_claims"),
            "roles": result.get("id_token_claims").get("roles", [])
        }
    else:
        return {
            "error": result.get("error"),
            "error_description": result.get("error_description"),
            "correlation_id": result.get("correlation_id")
        }   
