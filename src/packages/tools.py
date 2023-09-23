import numpy as np

"""
Gate data representation:

    "GATE": {
        "NAME": str
        "QUBITS": int,
        "BLOCKS": {
            "B1": {
                "index": int,
                "name": str,
                "ctrl": [int]?,
            }
            "B2": {
                ...
            },
            ...
        }
    }
"""

def prepare_initial_state(qubit_amount):
    matrix = np.array([1, 0])
    for _ in range(qubit_amount - 1):
        matrix = np.kron(matrix, np.array([1, 0]))
    return matrix

def get_gate_by_name(gate_name):
    if gate_name == "X":
        return np.array([[0, 1], [1, 0]])
    if gate_name == "Y":
        return np.array([[0, -1j], [1j, 0]])
    if gate_name == "Z":
        return np.array([[1, 0], [0, -1]])
    if gate_name == "H":
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    if gate_name == "SWAP":
        return np.array([[1, 0, 0, 0],
                         [0, 0, 1, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1]])

class Gate:
    """
    Gate class represented by its type and control indexes.

    Attributes
    ----------
    gate_name : str
        gate identifier
    gate : np.array
        gate array
    ctrl : [int]?
        list of control qubit's indexes
    """
    def __init__(self, gate_name, ctrl, gate):
        self.gate_name = gate_name
        self.gate = gate if gate is not None else get_gate_by_name(gate_name) 
        self.ctrl = ctrl

    def get_ctrl(self):
        return self.ctrl

    def get_gate_name(self):
        return self.gate_name
    
    def get_gate(self):
        return self.gate
    
    def set_gate(self, gate):
        self.gate = gate
    
    def set_ctrl(self, ctrl):
        self.ctrl = ctrl