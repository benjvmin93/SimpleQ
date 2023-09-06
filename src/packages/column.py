import numpy as np

from src.packages.gate import Gate

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

    def __init__(self, index, type, ctlr=None):
        """
        Parameters
        ----------
        index : int
            qubit index
        type : str
            gate identifier
        ctlr : [int]?
            control qubit indexes list
        """
        self.index = index
        self.gate = Gate(type, ctlr)
    
    def get_gate(self):
        return self.gate
    
    def get_index(self):
        return self.index
    
    def apply_column(self, quantum_register):
        qubit = quantum_register[self.index]
        qubit_state_vector = qubit.get_state_vector()
        controls = self.gate.get_ctrl()
        if controls:
            for control in controls:
                control_qubit = quantum_register[control]
                if control_qubit.get_beta() != 1:
                    return
        print(qubit_state_vector)
        qubit.set_state_vector(qubit_state_vector @ self.gate.get_gate_matrix())
        print(qubit.get_state_vector())