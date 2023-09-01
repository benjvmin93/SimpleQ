import numpy as np

class Qubit:
    def __init__(self):
        """
        By default, a qubit is initialized in the state |0>
        """
        self.ALPHA = 1 + 0 * 1j
        self.BETA = 0 + 0 * 1j

    def get_state_vector(self):
        return np.array([[self.ALPHA, self.BETA]])

    def get_alpha(self):
        return self.ALPHA

    def get_beta(self):
        return self.BETA
    
    def set_alpha(self, alpha):
        self.ALPHA = alpha
        
    def set_beta(self, beta):
        self.BETA = beta

    def print_state(self):
        print(f"{self.ALPHA}|0> + {self.BETA}|1>")