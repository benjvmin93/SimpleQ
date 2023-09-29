import numpy as np

from src.packages.tools import Gate, get_gate_by_name, get_control_matrix, build_unitary
from src.packages.logger import LogLevels, logger

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

    def __init__(self, index, gate_name, ctrl=None):
        """
        Parameters
        ----------
        index : int
            qubit index
        gate_name : str
            gate identifier
        ctrl : int?
            control qubit index
        """
        self.qubit_index = index
        self.gate = Gate(gate_name, ctrl)

    def get_gate(self):
        return self.gate
    
    def get_index(self):
        return self.qubit_index
    
    def apply_column(self, system_matrix, len_register):
        control = self.gate.get_ctrl()
        index = self.get_index()
        gate_name = self.get_gate().get_gate_name()
        gate = None
        
        log_control = f"with control {control}" if control is not None else f"without control"
        logger.log(f"Applying matrix {gate_name} on qubit {index} {log_control}", LogLevels.INFO)
        if control is not None:
            gate = get_control_matrix(self.get_gate()) # Control matrix on 2 qubits
            logger.log(f"Column-apply_column : control matrix : {gate}", LogLevels.DEBUG)
        else:
            gate = get_gate_by_name(self.get_gate().get_gate_name())


        gate = build_unitary(gate, len_register, index, control)            
            
        logger.log(f"Column-apply_column : Unitary gate : {gate}", LogLevels.DEBUG)
        system_matrix = gate @ system_matrix
        
        logger.log(f"Column-apply_column : New system vector obtained : {system_matrix}", LogLevels.DEBUG)
        
        return system_matrix / np.linalg.norm(system_matrix)