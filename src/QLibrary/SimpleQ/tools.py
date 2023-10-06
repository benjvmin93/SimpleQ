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

def get_SWAP_gate():
    return np.array([[1, 0, 0, 0], 
                     [0, 0, 1, 0], 
                     [0, 1, 0, 0], 
                     [0, 0, 0, 1]])

def get_control_matrix(gate, len_controls):
    control_gate = np.identity(2 ** (len_controls + 1))
    gate = get_gate_by_name(gate.get_name())
    identity_rows, identity_cols = control_gate.shape
    inserted_rows, inserted_cols = gate.shape   
    control_gate[identity_rows - inserted_rows:, identity_cols - inserted_cols:] = gate
    return control_gate

def get_swap_unitary(len_register, q0, q1):
    """
        Handles non-adjacent qubit SWAP.
        
        Parameters
        ----------
        len_register : int
            quantum register length
        q0, q1 : int
            qubit to swap indexes
    """
    if q0 < 0 or q0 >= len_register or q1 < 0 or q1 >= len_register:
        raise ValueError("Invalid qubit index")
    
    SWAP_gate = get_SWAP_gate()
    unitary = 1
    min_qubit = min(q0, q1)
    max_qubit = max(q0, q1)
    permutation_matrices = []
    permutation_matrix = 1
    
    dist = max_qubit - min_qubit
    # Build permutation matrices
    for i in range(dist):
        permutation_matrix = np.kron(np.identity(2**((len_register - 1) - max_qubit)), permutation_matrix)
        permutation_matrix = np.kron(SWAP_gate, permutation_matrix)
        max_qubit -= 1
        dist = max_qubit - min_qubit
        permutation_matrix = np.kron(np.identity(2 ** max_qubit), permutation_matrix)
        permutation_matrices.append(permutation_matrix)
        permutation_matrix = 1
    # Build unitary
    unitary = permutation_matrices[0]
    for perm_matrix in permutation_matrices[1:]:
        unitary = unitary @ perm_matrix
    for perm_matrix in permutation_matrices[:-1]:
        unitary = unitary @ perm_matrix
    
    return unitary

def build_unitary(gate_matrix, len_register, target_index, control_indexes=[]):
    unitary = 1
    for i in reversed(range(len_register)):
        if i in control_indexes:
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

    def get_name(self):
        return self.gate_name
    
    def get_gate(self):
        return self.gate