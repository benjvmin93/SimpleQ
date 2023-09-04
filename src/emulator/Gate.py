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

class Gate():
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
        return np.array([[1, 1], [1, -1]]) * 1 / np.sqrt(2)
    
    def get_gate_matrix(self):
        match self.type:
            case "X":
                return self.X()
            case "Y":
                return self.Y()
            case "Z":
                return self.Z()
            case "H":
                return self.H()
            case _:
                raise f"invalid gate type {self.type}"