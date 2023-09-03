import numpy as np

from Gate import Gate

class Column:
    def __init__(self, index, type, ctlr=None):
        self.index = index
        self.gate = Gate(type, ctlr)
    
    def get_gate(self):
        return self.gate
    
    
    
    def get_index(self):
        return self.index
    
    def apply_column(self, quantum_register):
        qubit = quantum_register[self.index]
        qubit_state_vector = qubit.get_state_vector()
        controls = self.gate.get_ctrl()
        if controls:
            for control in controls:
                control_qubit = quantum_register[control]
                if control_qubit.get_beta() != 1:
                    return
        qubit.set_state_vector(qubit_state_vector @ self.gate.get_gate_matrix())
        
        