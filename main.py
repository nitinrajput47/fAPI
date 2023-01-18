from fastapi import FastAPI, status, Response, HTTPException, Depends
from typing import Optional, List
import schemas
import json
import os
import uvicorn
from routers import user, authentication
import oauth

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)

def repeat(data,limit):
    lis = []
    for i in range(limit):
        lis.append(data)
    return lis

@app.get("/",status_code=status.HTTP_200_OK)
def home():
    return {"data":{"title":"Welcome","subject":"@copyright reserved by Nitin Rajput"}}

@app.get("/show/{id}", status_code=status.HTTP_200_OK, response_model=List[schemas.Show])
def show(id:int, response: Response,limits:int = 1, isCool:bool = True, level: Optional[int]=None, current_user: schemas.User = Depends(oauth.get_current_user)):
    fileName = "data.json"
    id = str(id)
    if not os.path.exists(fileName):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data available")
    else:
        response.status_code = status.HTTP_200_OK
        data = None
        with open(fileName,"r") as t:
            data = json.loads(t.read())
        if data.get(id):
            data = {"id":id,"data":data[id]}
            if level:
                data["data"]["level"]=level
            if isCool:
                if data["data"]["gender"]=="Male":
                    data["data"]["isCool"]="SuperCool"
                    return repeat(data,limits)
            else:
                data["data"]["isCool"]="cool"
                return repeat(data,limits)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not available with this ID")

@app.post("/create/",status_code=status.HTTP_201_CREATED)
def create(request: schemas.Create):
    fileName = "data.json"
    if os.path.exists(fileName):
        data = None
        with open(fileName,"r") as t:
            data = json.loads(t.read())
            max_id = max(data.keys())
            data[int(max_id)+1]={"name":request.name,"age":request.age,"gender":request.gender}
        with open(fileName,"w") as w:
            w.write(json.dumps(data))
    else:
        data = {}
        data[1]={"name":request.name,"age":request.age,"gender":request.gender}
        with open(fileName,"w") as w:
            w.write(json.dumps(data))

@app.delete("/del/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:str):
    fileName = "data.json"
    if os.path.exists(fileName):
        data = None
        with open(fileName,"r") as t:
            data = json.loads(t.read())
        if data.get(id):
            del data[id]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")
        with open(fileName,"w") as w:
            w.write(json.dumps(data))
        return {"data":"Record deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found")


# if __name__=="__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8080)
