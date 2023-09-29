import numpy as np

class Qubit:
    def __init__(self):
        """
        By default, a qubit is initialized in the state |0>
        """
        self.state_vector = np.array([1, 0], dtype=complex)

    def get_state_vector(self):
        return self.state_vector()

    def set_state_vector(self, state_vector):
        self.state = state_vector