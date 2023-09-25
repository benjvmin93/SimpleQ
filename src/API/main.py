from fastapi import FastAPI, Depends, HTTPException, Body

from fastapi_sqlalchemy import DBSessionMiddleware, db

import os

############ EMULATOR LIBRARY ############

from SimpleQ import circuit as circuit_object

############ SCHEMAS & MODELS #############

# import all Types here
from src.API.backend.schema import Circuit, User, Qbits_nb, Gate
from src.API.backend.models import Circuit as CircuitModel
from src.API.backend.models import User as UserModel


############# VALIDATORS ####################

from src.API.backend.validators import circuit_validator, gate_validator


############ INIT THE API #################


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

@app.post("/user/", response_model=User)
async def register_user(user: User):
    db_circuit = UserModel(username=user.username)
    db.session.add(db_circuit)
    db.session.commit()
    return db_circuit


# INIT Circuit    (qbit_amount : int) => new Circuit JSON

@app.post("/circuit/create/", response_model=Circuit)
async def create_circuit(qubits_nb: Qbits_nb):
    # create circuit object
    new_circuit = circuit_object.Circuit(qubits_nb.nb)
    # add circuit to database
    res = push_circuit_to_db(new_circuit)
    new_circuit = new_circuit.circuit_to_json()
    new_circuit['id'] = res.id
    # the id of the object is stored here, we have to discuss how we plan to store it in the workflow of the user
    return new_circuit


# ADD/DELETE qubit     (index : int, circuit) => Modified Circuit JSON


@app.post("/circuit/add/{index}", response_model=Circuit)
async def add_qubit(index: int, circuit: Circuit):
    # we verify if the circuit is the right format and if it exists in the database and convert it to a Circuit object
    circuit = circuit_validator(circuit)
    circuit.add_qubit(index)
    # ADD TO DATABASE
    # await push_circuit_to_db(circuit)   // TODO > find a way to store the id

    return circuit.circuit_to_json()


@app.post("/circuit/delete/{index}", response_model=Circuit)
async def delete_qubit(index: int, circuit: Circuit):
    # we verify if the circuit is the right format and if it exists in the database and convert it to a Circuit object
    circuit = circuit_validator(circuit)
    circuit.delete_qubit(index)
    # ADD TO DATABASE
    # await push_circuit_to_db(circuit)
    # TODO
    return circuit.circuit_to_json()


# SET gate     (gate_name : str, index : int, ctrl : list/None) => None/ ?

@app.post("/circuit/set_gate/{index}", response_model=Circuit)
async def set_gate(index: int, circuit: Circuit, gate: Gate):
    # we verify if the circuit is the right format and if it exists in the database and convert it to a Circuit object
    circuit = circuit_validator(circuit)
    gate = gate_validator(gate)
    circuit.set_gate(gate.gate_name, index, gate.ctrl_qubits_indexes)
    # ADD TO DATABASE
    # TODO
    return circuit.circuit_to_json()


# CREATE gate (gate_model : gate_model_type) => Gate : Gate_Type

# This will the fruit of a future update ! TODO


# LAUNCH circuit () => ? To define TODO


# Function for the Database


def push_circuit_to_db(circuits: Circuit) -> CircuitModel:
    db_circuit = CircuitModel(circuit=circuits.circuit_to_json())
    db.session.add(db_circuit)
    db.session.commit()
    return db_circuit
