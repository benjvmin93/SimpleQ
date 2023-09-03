from pydantic import BaseModel


class TestType(BaseModel):
    name: str


# A Gate has its type and the indexes of the control qbits (can be empty as well)
class Gate(BaseModel):
    type: str
    ctrl: list[int]


# One Column is equivalent to one action, it has the index of the qubit on which we take action and the Gate
class Column(BaseModel):
    index: int
    gate: Gate


# The type of the whole circuit, a list of sequential Columns which will be run one by one.
class Circuit(BaseModel):
    circuit: list[Column]
