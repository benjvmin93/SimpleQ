from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from fastapi_sqlalchemy import DBSessionMiddleware, db

import os
from dotenv import load_dotenv

############ SCHEMAS & MODELS #############

# import all Types here
from src.API.backend.schema import Circuit, User
from src.API.backend.models import Circuit as CircuitModel
from src.API.backend.models import User as UserModel

############ INIT THE API #################


dotenv_path = os.path.join(os.path.dirname(__file__), '../..', '.env')
load_dotenv(dotenv_path)

DB_PSWD = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')

DATABASE_URL = "postgresql://postgres:" + str(DB_PSWD) + "@postgres-container/" + str(DB_NAME)

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)


#################### GET REQUESTS ################
@app.get("/")
async def root():
    return {"message": "Hello lrd"}


@app.get("/circuit/")
async def get_circuits():
    circuits = db.session.query(CircuitModel).all()
    return circuits

@app.get("/users/")
async def get_users():
    users = db.session.query(UserModel).all()
    return users

################### POST REQUESTS ##################
@app.post("/")
async def send_test(circuit: Circuit):
    try:
        print(Circuit.name)
        return "all good"
    except ValidationError as e:
        error_message = e.errors()
        raise HTTPException(status_code=400, detail=error_message)


@app.post("/circuit/", response_model=Circuit)
async def create_circuit(circuit: Circuit):
    db_circuit = CircuitModel(name=circuit.name)
    db.session.add(db_circuit)
    db.session.commit()
    return db_circuit


@app.post("/user/", response_model=User)
async def register_user(user: User):
    db_circuit = UserModel(username=user.username)
    db.session.add(db_circuit)
    db.session.commit()
    return db_circuit
