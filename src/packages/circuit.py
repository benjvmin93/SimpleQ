from src.packages.column import Column
from src.packages.qubit import Qubit

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
    classical_register : list[int]
        used after measurement
    circuit : list[Column]
        gates representation
    """

    def __init__(self, qubit_amount):
        self.quantum_register = [Qubit() for _ in range(qubit_amount)]
        self.classical_register = [None for _ in range(qubit_amount)]
        self.circuit = []
    
    def get_quantum_register(self):
        return self.quantum_register
    
    def get_classical_register(self):
        return self.classical_register
    
    def set_gate(self, type, index, custom_gate=None, ctrl=None):
        """
        Add a gate to the circuit.
        Parameters
        ----------
        type : str
            gate identifier
        index : int
            qubit index,
        ctrl : [int]?
            control qubit indexes
        columns : [Column]?
            column list for custom gates. Only checked if type == "custom"
        """

        if type == "custom":
            if custom_gate == None:
                raise ValueError(custom_gate)
            self.circuit.extend(custom_gate)
        else:
            column = Column(index, type, ctrl)
            self.circuit.append(column)
        return self

    def create_gate(self, gate_model) -> list[Column]:
        """
        Create a custom gate
        Parameters
        ----------
        gate_model : dict
            Gate data representation
        """
        columns = []
        for block in gate_model["BLOCKS"]:
            columns.append(Column(block["index"], block["type"], block["ctrl"]))
        return columns
    
    def launch_circuit(self):
        for column in self.circuit:
            column.apply_column(self.quantum_register)
            
    def print_results(self):
        for qubit in self.quantum_register:
            qubit.print_state()
    
    def print_circuit(self):
        qubit_str = ["|0>" for _ in range(len(self.quantum_register))]
        for column in self.circuit:
            index = column.get_index()
            gate = column.get_gate()
            qubit_str[index] += f"--{gate.get_type()}"
        for q in qubit_str:
            print(q)
