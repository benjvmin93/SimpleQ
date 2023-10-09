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
        index = self.get_index()
        controls = gate.get_ctrl()

        log_control = f"with control {controls}" if controls != [] else f"without control"
        logger.log(f"Applying matrix {gate.get_name()} on qubit {index} {log_control}", LogLevels.INFO)
        
        gate_matrix = get_gate_by_name(gate.get_name())
        gate_matrix = build_unitary(gate_matrix, len_register, index, controls)

        logger.log(f"Control gate: {gate_matrix}", LogLevels.DEBUG)
        whole_unitary = np.identity(2 ** len_register)        

        if controls == []:
            whole_unitary = whole_unitary @ gate_matrix
        else:
            swap_matrices = []
            for control in controls:
                pos = control
                # Transpiler job
                if control > index or control < index - len(controls):
                    while pos < index - len(controls):
                        logger.log(f"SWAP between {pos} and {pos+1}", LogLevels.DEBUG)
                        swap_matrices.append(get_swap_unitary(len_register, pos, pos + 1))
                        pos += 1
                    while pos >= index + 1:
                        logger.log(f"SWAP between {pos} and {pos-1}", LogLevels.DEBUG)
                        swap_matrices.append(get_swap_unitary(len_register, pos, pos - 1))
                        pos -= 1
            logger.log(f"Building control matrix for {gate.get_name()} gate and {len(controls)} controls", LogLevels.DEBUG)
            gate_matrix = get_control_matrix(gate, len(controls))
            gate_matrix = build_unitary(gate_matrix, len_register, index, controls)
            unitary = swap_matrices[0] if swap_matrices != [] else gate_matrix
            if swap_matrices != []:
                for swap_matrix in swap_matrices[1:]:
                    unitary = unitary @ swap_matrix
                unitary = unitary @ gate_matrix
                for swap_matrix in reversed(swap_matrices):
                    unitary = unitary @ swap_matrix
            whole_unitary = whole_unitary @ unitary

        logger.log(f"Whole unitary: {whole_unitary} @ {system_matrix}", LogLevels.DEBUG)
        system_matrix = whole_unitary @ system_matrix
        
        return system_matrix / np.linalg.norm(system_matrix)