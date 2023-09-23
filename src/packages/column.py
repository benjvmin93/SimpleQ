import numpy as np

from src.packages.tools import Gate
from src.packages.tools import get_gate_by_name

def get_control_matrix(gate):
    gate = get_gate_by_name(gate.get_gate_name())
    control_gate = np.identity(4)
    identity_rows, identity_cols = control_gate.shape
    inserted_rows, inserted_cols = gate.shape   
    
    control_gate[identity_rows - inserted_rows:, identity_cols - inserted_cols:] = gate
    
    return control_gate

def build_unitary(gate_matrix, len_register, target_index, control_index):
    for i in range(len_register):
        if i == control_index:
            continue
        if i < target_index:
            gate_matrix = np.kron(np.identity(2), gate_matrix)
        if i > target_index:
            gate_matrix = np.kron(gate_matrix, np.identity(2))
    return gate_matrix


class Column:
    """
    A class used to represent one step within the circuit.

    Attributes
    ----------
    index : int
        the qubit on which the gate is applied
    gate : Gate
        the quantum gate we are applying at this specific index
    """

    def __init__(self, index, gate_name, ctlr=None, gate_matrix=None):
        """
        Parameters
        ----------
        index : int
            qubit index
        gate_name : str
            gate identifier
        ctlr : [int]?
            control qubit indexes list
        gate_matrix : np.array([])?
            unitary gate matrix
        """
        self.qubit_index = index
        self.gate = Gate(gate_name, ctlr, gate_matrix)

    def get_gate(self):
        return self.gate
    
    def get_index(self):
        return self.qubit_index
    
    def apply_column(self, system_matrix, len_register):
        controls = self.gate.get_ctrl()
        index = self.get_index()
        gate_name = self.get_gate().get_gate_name()

        print(f"Applying matrix {gate_name} on qubit {index}", f"with controls {controls}" if controls else f"without controls")
        

        if controls:
            for control in controls:
                control_gate = get_control_matrix(self.get_gate()) # Control matrix on 2 qubits    
                control_gate = build_unitary(control_gate, len_register, index, control)
                system_matrix = control_gate @ system_matrix
        else:
            gate = get_gate_by_name(self.get_gate().get_gate_name())
            gate = build_unitary(gate, len_register, index, -1)
            system_matrix = system_matrix @ gate

        print(f"New system vector obtained :", system_matrix)
        return system_matrix 