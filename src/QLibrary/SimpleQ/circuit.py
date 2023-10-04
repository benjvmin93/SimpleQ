import numpy as np

from src.QLibrary.SimpleQ.column import Column
from src.QLibrary.SimpleQ.tools import get_gate_by_name
from src.QLibrary.SimpleQ.tools import prepare_initial_state
from src.QLibrary.SimpleQ.tools import Gate
from src.QLibrary.SimpleQ.qubit import Qubit

import json

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
        self.circuit = []
        self.gate_register = []
        self.system_matrix = prepare_initial_state(qubit_amount)

    def circuit_to_json(self):
        circ = []
        for column in self.circuit:
            circ.append(column.column_to_json())
        circuit_json = {
            "nb_qubit": str(len(self.quantum_register)),
            "circuit": circ
        }
        return circuit_json

    def get_quantum_register(self):
        return self.quantum_register

    def get_gate_register(self):
        return self.gate_register

    def get_system_matrix(self):
        return self.system_matrix

    def add_qubit(self, index):
        self.quantum_register.insert(index, Qubit())

    def delete_qubit(self, index):
        self.quantum_register.pop(index)

    def set_gate(self, gate_name, index, ctrl=[]):
        """
        Add a gate to the circuit.
        Parameters
        ----------
        gate_name : str
            gate identifier
        index : int
            qubit index
        columns : [Column]?
            column list for custom gates
        ctrl : [int]?
            control qubit indexes
        """

        implemented_gates = ["X", "Y", "Z", "H", "SWAP"]
        if gate_name in implemented_gates:
            self.circuit.append(Column(index, gate_name, ctrl))
            return self
        """
        for gate in self.gate_register:
            if gate_name == gate.get_gate_name():
                self.circuit = []
        """

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
        qubit_matrices = [np.identity(2) for _ in range(
            circuit_qubits)]  # Create a list of gate matrices that have to be applied for each qubits in the system

        for block in reversed_block_list:
            qubit_matrix = qubit_matrices[block["index"]]  # Get the right qubit which the gate will be applied on
            qubit_matrices[block["index"]] = np.dot(qubit_matrix, get_gate_by_name(
                block["name"]))  # compute matrices multiplication between the two gate matrices

        unitary = None  # Initialize the unitary gate that will apply all our gate to the global system
        for m in qubit_matrices:  # Iterate through our gate matrices
            if unitary is None:  # set the unitary to the gate matrix (only occurs at the first iteration)
                unitary = m
            else:
                unitary = np.kron(unitary, m)  # Apply tensor product of our unitary with the gate matrix.
                # Works because if the qubit matrix hasn't been touched, we end up with identity matrices
                # corresponding to no changes within the qubit state.
        gate = {  # Finally add our custom gate to the gate_register. It can be retrieve by its name.
            "name": gate_model["NAME"],
            "matrix": unitary
        }
        self.gate_register.append(gate)

        return gate

    def launch_circuit(self):
        for column in self.circuit:
            column.apply_column(self.quantum_register)

    def print_results(self):
        for qubit in self.quantum_register:
            qubit.print_state()

    def pretty_print(self):
        m = [["-----" for _ in range(len(self.circuit))] for _ in range(len(self.quantum_register))]
        i = 0
        for col in self.circuit:
            m[col.get_index()][i] = f"[ {col.get_gate().get_gate_name()[0]} ]"
            for ctrl in col.get_gate().get_ctrl():
                m[ctrl][i] = f"- * -"
            i += 1
        for line in m:
            print("|0> -", end="")
            for col in line:
                print(col, end="-")
            print()

    @staticmethod
    def json_to_circuit(json_element):
        circuit_data = json.loads(json_element)
        nb_qubit = circuit_data["nb_qubit"]
        columns_data = circuit_data["circuit"]
        circuit = Circuit(nb_qubit)
        for column in columns_data:
            data = json.loads(column)
            gate_data = json.loads(data["qubit_information"])
            circuit.set_gate(gate_data["gate_name"], data["qubit_index"], gate_data["ctrl_qubits_indexes"])
        return circuit



