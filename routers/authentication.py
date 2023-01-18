from fastapi import APIRouter, HTTPException, status, Depends
import schemas
from passlib.context import CryptContext
import json
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)
JWT_KEY = "sd9fi803,*(##89CWD548W"
pwt_ctxt = CryptContext(schemes=["bcrypt"])

@router.post("/token",status_code=status.HTTP_200_OK)
def authenticate(request: OAuth2PasswordRequestForm = Depends()):
    email = request.username
    password  = request.password
    with open("user.json","r") as t:
        data = json.loads(t.read())
    if not data.get(email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
    if not pwt_ctxt.verify(password,data[email]["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    bearer = jwt.encode({"data":data[email],"exp":datetime.now(tz=timezone.utc)+timedelta(seconds = 30)},JWT_KEY)
    return {"access_token":bearer, "token_type":"bearer"}