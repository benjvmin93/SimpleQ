import numpy as np

from src.QLibrary.SimpleQ import Column
from src.QLibrary.SimpleQ.tools import *
from src.QLibrary.SimpleQ.qubit import Qubit
from src.QLibrary.SimpleQ.logger import *

class Circuit:
    """
    A class used to represent a Circuit. A circuit is represented by its column list.

    Attributes
    ----------
    quantum_register : list[Qubit]
        qubits stockage
    circuit : list[Column]
        gates representation
    gate_register : list[Gate]
        custom gates
    """

    def __init__(self, qubit_amount):
        self.quantum_register = [Qubit() for _ in range(qubit_amount)]
        self.system_matrix = prepare_initial_state(qubit_amount)
        self.circuit = []
        self.gate_register = []
        logger.log(f"Circuit - __init__: created new circuit with {str(len(self.quantum_register))} qubits.", LogLevels.INFO)
        logger.log(f"Circuit - __init_: system matrix : {self.system_matrix}", LogLevels.DEBUG)

    def get_quantum_register(self):
        return self.quantum_register
    
    def get_gate_register(self):
        return self.gate_register
    
    def get_system_matrix(self):
        return self.system_matrix
    
    def add_qubit(self, index=None):
        if index is None:
            self.quantum_register.append(Qubit())
        else:
            self.quantum_register.insert(index, Qubit())

    def delete_qubit(self, index):
        self.quantum_register.pop(index)

    def update_qubits(self):
        """
            Update qubit amplitudes using the system matrix.
        """
        # Reset qubit values (no worries because the new information are encoded in the system_matrix)
        for qubit in self.quantum_register:
            qubit.set_alpha(0)
            qubit.set_beta(0)

        # iterate through every possible states
        for i in range(2 ** len(self.quantum_register)):
            bitstring = str(bin(i)[2:]).zfill(len(self.quantum_register))
            # iterate through bitstring
            for j in range(len(bitstring)):
                qubit_val = int(bitstring[j])
                qubit = self.quantum_register[j]
                
                logger.log(f"Circuit-update_qubits : state |{bitstring}>, qubit {j}", LogLevels.DEBUG)
                
                amplitude = np.abs(self.system_matrix[i] ** 2) * (self.system_matrix[i] / np.abs(self.system_matrix[i])) if self.system_matrix[i] != 0 else 0 # Using this formula, we conserve the negative values
                
                logger.log(f"Circuit-update_qubits : system_matrix[{i}] = {self.system_matrix[i]}. Computed amplitude = {amplitude}", LogLevels.DEBUG)
                 
                if qubit_val == 0: # If qubit is |0> then we need to update amplitude alpha
                    qubit.set_alpha(qubit.get_alpha() + amplitude)
                if qubit_val == 1: # If qubit is |1> then we need to update amplitude beta
                    qubit.set_beta(qubit.get_beta() + amplitude)
                self.quantum_register[j] = qubit # Keep track of the qubit in the register
        # Don't forget to normalize
        for j in range (len(self.quantum_register)):
            alpha = self.quantum_register[j].get_alpha()
            beta = self.quantum_register[j].get_beta()
            alpha = np.sqrt(np.abs(alpha)) * (alpha / np.abs(alpha)) if alpha != 0 else 0
            beta = np.sqrt(np.abs(beta)) * (beta / np.abs(beta)) if beta != 0 else 0
            qubit.set_alpha(alpha)
            qubit.set_beta(beta)
            logger.log(f"Circuit-update_qubits : qubit {j} = {qubit.get_str_state()}.", LogLevels.DEBUG)

    def set_gate(self, gate_name, index, ctrl=None):
        """
        Add a gate to the circuit.
        Parameters
        ----------
        gate_name : str
            gate identifier
        index : int
            qubit index
        ctrl : int?
            control qubit index
        """
        
        implemented_gates = ["X", "Y", "Z", "H"]
        if gate_name not in implemented_gates:
            raise NameError(f"{gate_name} gate not found")
        self.circuit.append(Column(index, gate_name, ctrl))
        logger.log(f"Circuit-set_gate : added {gate_name} gate at index {index}", LogLevels.INFO)
        return self
    
    def create_gate(self, gate_model) -> Gate:
        """
        Create a custom gate
        Parameters
        ----------
        gate_model : dict
            Gate data representation
        """

        # Reverse block list so we compute the gate unitary matrix from right to left in the circuit.
        reversed_block_list = []
        for block in gate_model["BLOCKS"]:
            reversed_block_list.append(block)
        reversed_block_list.reverse()
        
        circuit_qubits = len(self.quantum_register)
        qubit_matrices = [np.identity(2) for _ in range(circuit_qubits)] # Create a list of gate matrices that have to be applied for each qubits in the system
        
        for block in reversed_block_list:
            qubit_matrix = qubit_matrices[block["index"]] # Get the right qubit which the gate will be applied on
            qubit_matrices[block["index"]] = np.dot(qubit_matrix, get_gate_by_name(block["name"])) # compute matrices multiplication between the two gate matrices
            
        unitary = None # Initialize the unitary gate that will apply all our gate to the global system
        for m in qubit_matrices: # Iterate through our gate matrices
            if unitary is None: # set the unitary to the gate matrix (only occurs at the first iteration)
                unitary = m
            else:
                unitary = np.kron(unitary, m)   # Apply tensor product of our unitary with the gate matrix.
                                                # Works because if the qubit matrix hasn't been touched, we end up with identity matrices corresponding to no changes within the qubit state.
        gate = {    # Finally add our custom gate to the gate_register. It can be retrieve by its name.
            "name": gate_model["NAME"],
            "matrix": unitary
        }
        self.gate_register.append(gate)
        
        return gate

    def launch_circuit(self):
        for column in self.circuit:
            self.system_matrix = column.apply_column(self.system_matrix, len(self.quantum_register))
        logger.log(f"Circuit-launch_circuit : Final obtained vector state : {self.system_matrix}", LogLevels.INFO)

    def print_results(self):
        for qubit in self.quantum_register:
            print(qubit.get_str_state())
    
    def print_circuit(self):
        qubit_str = ["|0>" for _ in range(len(self.quantum_register))]
        for column in self.circuit:
            index = column.get_index()
            gate = column.get_gate()
            qubit_str[index] += f"--{gate.get_type()}"
        for q in qubit_str:
            print(q)
