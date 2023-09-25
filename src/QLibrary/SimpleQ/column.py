import numpy as np

from src.QLibrary.SimpleQ.tools import Gate
from src.QLibrary.SimpleQ.tools import get_gate_by_name, get_control_matrix, build_unitary
from src.QLibrary.SimpleQ.logger import LogLevels

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

    def __init__(self, logger, index, gate_name, ctrl=None):
        """
        Parameters
        ----------
        logger : Logger
            logger instance
        index : int
            qubit index
        gate_name : str
            gate identifier
        ctrl : int?
            control qubit index
        """
        self.qubit_index = index
        self.gate = Gate(gate_name, ctrl)
        self.logger = logger

    def column_to_json(self):
        column_json = {
            "qubit_index": str(self.qubit_index),
            "qubit_information": self.gate.gate_to_json()
        }
        return column_json

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
        self.logger.log(f"Applying matrix {gate_name} on qubit {index} {log_control}", LogLevels.INFO)
        if control is not None:
            gate = get_control_matrix(self.get_gate()) # Control matrix on 2 qubits
            self.logger.log(f"Column-apply_column : control matrix : {gate}", LogLevels.DEBUG)
        else:
            gate = get_gate_by_name(self.get_gate().get_gate_name())
            self.logger.log(f"Column-apply_column : Unitary gate : {gate}", LogLevels.DEBUG)
        
        gate = build_unitary(gate, len_register, index, control)
        self.logger.log(f"Column-apply_column : Unitary gate : {gate}", LogLevels.DEBUG)
        system_matrix = gate @ system_matrix
        
        self.logger.log(f"Column-apply_column : New system vector obtained : {system_matrix}", LogLevels.DEBUG)
        
        return system_matrix / np.linalg.norm(system_matrix)