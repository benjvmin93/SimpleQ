import numpy as np

"""
Gate data representation:

    "GATE": {
        "QUBITS": int,
        "BLOCKS": {
            "B1": {
                "index": int,
                "type": str,
                "ctrl": [int]?,
            }
            "B2": {
                ...
            },
            ...
        }
    }
"""

class Gate:
    """
    Gate class represented by its type and control indexes.

    Attributes
    ----------
    type : str
        gate identifier
    ctrl : [int]?
        list of control qubit's indexes
    """
    def __init__(self, type, ctrl):
        self.type = type
        self.ctrl = ctrl
        
    def get_ctrl(self):
        return self.ctrl
    
    def get_type(self):
        return self.type
        
    def X(self):
        return np.array([[0, 1], [1, 0]])
    
    def Y(self):
        return np.array([[0, -1j], [1j, 0]])
    
    def Z(self):
        return np.array([[1, 0], [0, -1]])
    
    def H(self):
        return np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    
    def SWAP(self):
        return np.array([[1, 0, 0, 0],
                         [0, 0, 1, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1]])
    
    def get_gate_matrix(self):
        gate_matrix = None
        match self.type:
            case "X":
                gate_matrix = self.X()
            case "Y":
                gate_matrix = self.Y()
            case "Z":
                gate_matrix = self.Z()
            case "H":
                gate_matrix = self.H()
            case "SWAP":
                gate_matrix = self.SWAP()
            case _:
                raise TypeError(f"invalid gate type {self.type}")
        return gate_matrix