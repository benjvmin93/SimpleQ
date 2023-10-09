import numpy as np

def prepare_initial_state(qubit_amount : int):
    """
    Initialize a vector state to `|0> ⊗ qubit_amount`
    """
    matrix = np.array([1, 0])
    for _ in range(qubit_amount - 1):
        matrix = np.kron(matrix, np.array([1, 0]))
    return matrix

def get_gate_by_name(gate_name : str):
    """
    Returns the gate matrix associated to its name.
    """
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
    """
    Returns SWAP gate matrix.
    This method is separated from the method `get_gate_by_name` because it handles a 2 qubit gate that is not intended to be part of the built-in gates.
    """
    return np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]])

def get_control_matrix(gate : np.array, len_controls : int):
    """
    Returns a control matrix according to the the corresponding gate and the number of controls.
    """
    control_gate = np.identity(2 ** (len_controls + 1))
    gate = get_gate_by_name(gate.get_name())
    identity_rows, identity_cols = control_gate.shape
    inserted_rows, inserted_cols = gate.shape
    control_gate[identity_rows - inserted_rows:, identity_cols - inserted_cols:] = gate
    return control_gate

def get_swap_unitary(len_register : int, q0: int, q1: int):
    """
    Returns a matrix unitary that performs a swap between two qubits.

    Handles non-adjacent qubit indexes.
    Parameters
    ----------
    len_register : quantum register length
    q0, q1 : qubit indexes to swap
    """
    if q0 < 0 or q0 >= len_register or q1 < 0 or q1 >= len_register:
        raise ValueError("Invalid qubit index")
    
    # Initialize all needed variables
    SWAP_gate = get_SWAP_gate() # SWAP gate
    unitary = 1 # final unitary
    min_qubit = min(q0, q1) # Maximum index
    max_qubit = max(q0, q1) # Minimum index
    permutation_matrices = [] # List to stock our permutations matrices that will be reused to put the qubits back to their original positions.
    permutation_matrix = 1
    
    dist = max_qubit - min_qubit
    
    # Build permutation matrices
    # To swap the qubits, we need to perform 'dist' permutations
    for _ in range(dist):
        permutation_matrix = np.kron(np.identity(2**((len_register - 1) - max_qubit)), permutation_matrix) # Start by building the unitary from the bottom of the circuit (ie. from the last qubit) to the SWAP gate 
        permutation_matrix = np.kron(SWAP_gate, permutation_matrix) # Add SWAP gate to the unitary
        max_qubit -= 1 # Update qubit position index
        dist = max_qubit - min_qubit # Update distance between the two qubits
        permutation_matrix = np.kron(np.identity(2 ** max_qubit), permutation_matrix) # Tensor product between the permutation matrix and identity with the size of the rest of the qubits that are not touched.
        permutation_matrices.append(permutation_matrix) # Append the permutation matrix to the list
        permutation_matrix = 1 # Set the permutation matrix back to 1

    # Build unitary
    # Here we multiply all the permutation matrices to get the whole unitary that will perform the full SWAP
    unitary = permutation_matrices[0]
    for perm_matrix in permutation_matrices[1:]:
        unitary = unitary @ perm_matrix
    for perm_matrix in permutation_matrices[:-1]:
        unitary = unitary @ perm_matrix
    
    return unitary

def build_unitary(gate_matrix : np.array, len_register : int, target_index : int, control_indexes : list=[]):
    """
    Build a unitary matrix according to a specific gate, the full register length, the gate's target qubit and optionally the control indexes
    """
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

def get_distribution(p0: float, p1: float, shots=1000):
    """
    Returns a distribution of 0 and 1 with 'shots' trials according to their probabilities.
    """
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
    Gate class represented by name and control indexes.

    Attributes
    ----------
    gate_name : gate identifier
    gate : gate array
    ctrl : list of control qubit's indexes
    """
    def __init__(self, gate_name : str, ctrl : list):
        self.gate_name = gate_name
        self.gate = get_gate_by_name(gate_name) 
        self.ctrl = ctrl

    def get_ctrl(self):
        return self.ctrl

    def get_name(self):
        return self.gate_name
    
    def get_gate(self):
        return self.gate