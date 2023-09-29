import numpy as np

from src.packages.column import Column
from src.packages.tools import Gate, get_gate_by_name, prepare_initial_state, build_unitary, get_distribution
from src.packages.qubit import Qubit
from src.packages.logger import *

"""
Circuit data representation:

    "CIRCUIT": {
        "QUBITS": int,
        "GATES": {
            "G1": ...,
            "G2": ...,
            ...
        }
    }
"""

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
        self.classical_register = [None for _ in range(qubit_amount)]
        logger.log(f"Circuit - __init__: created new circuit with {str(len(self.quantum_register))} qubits.", LogLevels.INFO)
        logger.log(f"Circuit - __init_: system matrix : {self.system_matrix}", LogLevels.DEBUG)

    def get_quantum_register(self):
        return self.quantum_register
    
    def get_gate_register(self):
        return self.gate_register
    
    def get_system_matrix(self):
        return self.system_matrix
    
    def get_classical_register(self):
        return self.classical_register

    def add_qubit(self, index=None):
        if index is None:
            self.quantum_register.append(Qubit())
        else:
            self.quantum_register.insert(index, Qubit())

    def delete_qubit(self, index):
        self.quantum_register.pop(index)

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
        
        implemented_gates = ["X", "Y", "Z", "H", "SWAP"]
        if gate_name not in implemented_gates:
            raise NameError(f"{gate_name} gate not found")
        self.circuit.append(Column(index, gate_name, ctrl))
        logger.log(f"Circuit-set_gate : added {gate_name} gate at index {index}", LogLevels.INFO)
        return self
    
    def measure(self, index, shots=1000, simulation=False):
        psi = self.system_matrix
        # Our measurement operators in the {|0>,|1>} basis
        M0 = np.array([[1, 0],
                       [0, 0]])
        M1 = np.array([[0, 0],
                       [0, 1]])

        # Build unitary measurement operators
        M0 = build_unitary(M0, len(self.quantum_register), index)
        M1 = build_unitary(M1, len(self.quantum_register), index)

        # Get associate probabilities to obtain 0 or 1
        p0 = psi.conjugate() @ M0.conjugate().T @ M0 @ psi
        p1 = psi.conjugate() @ M1.conjugate().T @ M1 @ psi
        
        results = {
            "proba": {
                "p0": p0,
                "p1": p1, 
            },
            "simulation" : None
        }
        if simulation == True:
            # Get probability statistics
            distribution = get_distribution(p0, p1, shots)
            # Perform measurement according to probabilities
            measure = np.random.choice([0, 1], size=1, p=[p0, p1])
            simulation = {
                "distribution": distribution,
                "measurement": measure[0]
            }
            results["simulation"] = simulation
            # Update state vector
            if measure[0] == 0:
                psi = (M0 @ psi) / np.sqrt(p0)
            else:
                psi = (M1 @ psi) / np.sqrt(p1)
            self.system_matrix = psi

        self.classical_register[index] = results
        return results

    def measure_all(self, shots=1000, simulation=False):
        for i in range(len(self.quantum_register)):
            self.measure(i, shots, simulation)
    
    def launch_circuit(self):
        for column in self.circuit:
            self.system_matrix = column.apply_column(self.system_matrix, len(self.quantum_register))
        logger.log(f"Circuit-launch_circuit : Final obtained vector state : {self.system_matrix}", LogLevels.INFO)
