import os

from fastapi import HTTPException, Body, FastAPI
from src.API.backend.schema import Circuit, Gate
from src.API.backend.models import Circuit as CircuirModel
from SimpleQ import circuit as circuit_object
from fastapi_sqlalchemy import DBSessionMiddleware, db


def circuit_validator(circuit: Circuit = Body(...)):
    c = None
    with db():
        c = db.session.query(CircuirModel).filter(CircuirModel.id == circuit.id).first()
    if c is None:
        raise HTTPException(status_code=404, detail="Circuit not found")
    try:
        circuit = circuit_object.json_to_circuit(circuit)
        return circuit
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON Circuit format")


def gate_validator(gate: Gate = Body(...)):
    try:
        return gate
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON Gate format")
