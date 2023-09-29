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
    if gate_name == "M":
        return np.array([[1, 0], [0, 0]])

def get_control_matrix(gate):
    gate = get_gate_by_name(gate.get_gate_name())
    control_gate = np.identity(4)
    identity_rows, identity_cols = control_gate.shape
    inserted_rows, inserted_cols = gate.shape   
    
    control_gate[identity_rows - inserted_rows:, identity_cols - inserted_cols:] = gate
    
    return control_gate

def build_unitary(gate_matrix, len_register, target_index, control_index=None):
    unitary = 1
    for i in range(len_register - 1, -1, -1):
        if control_index is not None and i == control_index:
            continue
        if i > target_index:
            unitary = np.kron(unitary, np.identity(2))
        if i == target_index:
            unitary = np.kron(gate_matrix, unitary)
        if i < target_index:
            unitary = np.kron(np.identity(2), unitary)
    return unitary

def get_distribution(p0, p1, shots=1000):
    result_0 = 0
    result_1 = 0
    for _ in range(shots):
        measure = np.random.choice([0, 1], size=1, p=[p0, p1])
        if measure[0] == 0:
            result_0 += 1
        else:
            result_1 += 1
    results = {
        "0": result_0,
        "1": result_1
    }
    
    return results

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
    def __init__(self, gate_name, ctrl):
        self.gate_name = gate_name
        self.gate = get_gate_by_name(gate_name) 
        self.ctrl = ctrl

    def get_ctrl(self):
        return self.ctrl

    def get_gate_name(self):
        return self.gate_name
    
    def get_gate(self):
        return self.gate