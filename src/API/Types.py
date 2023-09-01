from pydantic import BaseModel


class TestType(BaseModel):
    name: str


class Gate(BaseModel):
    type: str
    ctrl: list[int]


class Column(BaseModel):
    index: int
    gate: Gate


class Circuit(BaseModel):
    circuit: list[Column]
