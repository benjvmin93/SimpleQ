from Column import Column
from Qubit import Qubit

class Circuit:
    def __init__(self, qubit_amount):
        self.quantum_register = [Qubit() for _ in range(qubit_amount)]
        self.classical_register = [None for _ in range(qubit_amount)]
        self.circuit = []
    
    def get_quantum_register(self):
        return self.quantum_register
    
    def get_classical_register(self):
        return self.classical_register
    
    def set_gate(self, type, index, ctrl=None):
        column = Column(index, type, ctrl)
        self.circuit.append(column)
        return self

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
