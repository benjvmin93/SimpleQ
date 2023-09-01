import numpy as np
import Qubit 

class Circuit:
    def __init__(self, qubit_amount):
        self.quantum_register = [Qubit.Qubit() for _ in range(qubit_amount)]
        self.classical_register = [None for _ in range(qubit_amount)]
        self.circuit = [[] for _ in range(qubit_amount)]
        
    def get_quantum_register(self):
        return self.quantum_register
    
    def get_classical_register(self):
        return self.classical_register
    
    def X_callback(self, qubit):
        sigma_x = np.array([[0, 1], [1, 0]])
        state_vector = qubit.get_state_vector()
        result = state_vector @ sigma_x
        qubit.set_alpha(result[0][0])
        qubit.set_beta(result[0][1])
        return qubit
    
    def X(self, index):
        self.circuit[index].append(self.X_callback)
        return self
    
    def H_callback(self, qubit):
        hadamard = np.array([[1, 1], [1, -1]])
        state_vector = qubit.get_state_vector()
        result = state_vector @ hadamard
        qubit.set_alpha(result[0][0])
        qubit.set_beta(result[0][1])
        return qubit
    
    def H(self, index):
        self.circuit[index].append(self.H_callback)
        return self
    
    def print_circuit(self):
        circ_str = ""
        for i in range(len(self.quantum_register)):
            circ_str += "|0>--"
            for gate in self.circuit[i]:
                if gate.__name__ == "X_callback":
                    circ_str += "X--"
                elif gate.__name__ == "H_callback":
                    circ_str += "H--"
            circ_str += '\n'
        print(circ_str)