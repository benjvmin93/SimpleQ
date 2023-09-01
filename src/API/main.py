from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

# import all Types here
from src.API.Types import TestType

app = FastAPI()


#################### GET REQUESTS ################
@app.get("/")
async def root():
    return {"message": "Hello World"}


################### POST REQUESTS ##################
@app.post("/")
async def basic(test: TestType):
    try:
        print(test.name)
        return "all good"
    except ValidationError as e:
        error_message = e.errors()
        raise HTTPException(status_code=400, detail=error_message)
