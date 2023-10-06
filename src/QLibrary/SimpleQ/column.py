import numpy as np

from src.QLibrary.SimpleQ.tools import Gate
from src.QLibrary.SimpleQ.tools import get_gate_by_name, get_control_matrix, build_unitary, get_swap_unitary
from src.QLibrary.SimpleQ.logger import logger, LogLevels

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
    def __init__(self, index, gate_name, ctrl=[]):
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
        gate = self.get_gate()
        control = gate.get_ctrl()[0] if gate.get_ctrl() != [] else None
        index = self.get_index()
        
        swap_matrices = []
        log_control = f"with control {control}" if control is not None else f"without control"
        logger.log(f"Applying matrix {gate.get_name()} on qubit {index} {log_control}", LogLevels.INFO)

        if control is not None:
            # Transpiler job
            if control != index - 1:
                logger.log(f"control: {control}, index: {index}", LogLevels.DEBUG)
                while control < index - 1:
                    swap_matrices.append(get_swap_unitary(len_register, control, control + 1))
                    control += 1
                    logger.log(f"control: {control}, index: {index}", LogLevels.DEBUG)
                while control > index + 1:
                    swap_matrices.append(get_swap_unitary(len_register, control, control - 1))
                    control -= 1
                    logger.log(f"control: {control}, index: {index}", LogLevels.DEBUG)
                if control == index + 1:
                    swap_matrices.append(get_swap_unitary(len_register, control, index))
                logger.log(f"control: {control - 1}, index: {index + 1}", LogLevels.DEBUG)
            gate = get_control_matrix(gate) # Control matrix on 2 qubits
        else:
            gate = get_gate_by_name(gate.get_name())
        gate = build_unitary(gate, len_register, index, control)
        unitary = swap_matrices[0] if len(swap_matrices) != 0 else gate
        if swap_matrices != []:
            for swap_matrix in swap_matrices[1:]:
                unitary = unitary @ swap_matrix
            unitary = unitary @ gate
            for swap_matrix in reversed(swap_matrices):
                unitary = unitary @ swap_matrix

        logger.log(f"Column-apply_column : Unitary gate : {gate}", LogLevels.DEBUG)
        system_matrix = unitary @ system_matrix
        
        logger.log(f"Column-apply_column : New system vector obtained : {system_matrix}", LogLevels.DEBUG)
        
        return system_matrix / np.linalg.norm(system_matrix)