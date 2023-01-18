from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # import ipdb; ipdb.set_trace()
    try:
        JWT_KEY = "sd9fi803,*(##89CWD548W"
        payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        data = payload.get("data")
        name = data.get('name')
        passw = data.get("password")
        email = data.get("email")
        with open("/fAPI/user.json","r") as t:
            users = json.loads(t.read())
        if not users.get(email):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid Beare Token'
        )
        users = users.get(email)
        if name==users.get("name") and users.get("password")==passw:  # registered user
            return payload.get("data")
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid Bearer Token'
            )
    except Exception as e:
        if e.args==jwt.ExpiredSignatureError('Signature has expired').args:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Token Expired'
        )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid Bearer Token'
            )