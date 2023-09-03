from Column import Column
from Qubit import Qubit

class Circuit:
    def __init__(self, qubit_amount):
        self.quantum_register = [Qubit.Qubit() for _ in range(qubit_amount)]
        self.classical_register = [None for _ in range(qubit_amount)]
        self.circuit = [[] for _ in range(qubit_amount)]
    
    def get_quantum_register(self):
        return self.quantum_register
    
    def get_classical_register(self):
        return self.classical_register
    
    def X(self, index, ctrl):
        column = Column(index, "X", ctrl)
        self.circuit.append(column)
        return self
    
    def Y(self, index, ctrl):
        column = Column(index, "Y", ctrl)
        self.circuit.append(column)
        return self
    
    def Z(self, index, ctrl):
        column = Column(index, "Z", ctrl)
        self.circuit.append(column)
        return self

    def H(self, index, ctrl):
        column = Column(index, "H", ctrl)
        self.circuit.append(column)
        return self