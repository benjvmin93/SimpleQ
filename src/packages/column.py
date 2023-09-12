from src.packages.tools import Gate
from src.packages.tools import get_gate_by_name

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

    def __init__(self, index, gate_name, ctlr=None, gate=None):
        """
        Parameters
        ----------
        qubit_index : int
            qubit index
        gate_name : str
            gate identifier
        ctlr : [int]?
            control qubit indexes list
        """
        self.qubit_index = index
        self.gate = Gate(gate_name, ctlr, gate)

    def get_gate(self):
        return self.gate
    
    def get_index(self):
        return self.qubit_index
    
    def apply_column(self, quantum_register):
        qubit = quantum_register[self.qubit_index]
        qubit_state_vector = qubit.get_state_vector()
        controls = self.gate.get_ctrl()
        if controls:
            for control in controls:
                control_qubit = quantum_register[control]
                if control_qubit.get_beta() != 1:
                    return
        print(qubit_state_vector)
        qubit.set_state_vector(qubit_state_vector @ get_gate_by_name(self.gate.get_gate_name()))
        print(qubit.get_state_vector())