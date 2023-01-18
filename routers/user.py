from fastapi import APIRouter, status
import schemas
from passlib.context import CryptContext
import os
import json

router = APIRouter(
     tags=['User'],
     prefix="/user"
)
passCtxt = CryptContext(schemes=["bcrypt"])

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PassRes)
def create(request: schemas.User):
    fileName = "/fAPI/user.json"
    hashedPass = passCtxt.hash(request.password)
    if os.path.exists(fileName):
        data = None
        with open(fileName,"r") as t:
            data = json.loads(t.read())
            max_id = max(data.keys())
            data[request.email]={"name":request.name,"email":request.email,"password":hashedPass}
        with open(fileName,"w") as w:
            w.write(json.dumps(data))
    else:
        data = {}
        data[request.email]={"name":request.name,"email":request.email,"password":hashedPass}
        with open(fileName,"w") as w:
            w.write(json.dumps(data))
    return request