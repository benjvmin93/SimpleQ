from pydantic import BaseModel


class Index(BaseModel):
    index: int


class Gate(BaseModel):
    gate_name: str
    ctrl_qubits_indexes: list[int]

    class Config:
        orm_mode = True


class Column(BaseModel):
    qubit_index: int
    qubit_information: Gate

    class Config:
        orm_mode = True


class Circuit(BaseModel):
    id: int = None
    nb_qubit: int
    circuit: list[Column]

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class Qbits_nb(BaseModel):
    nb: int

    class Config:
        orm_mode = True
