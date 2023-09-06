import pytest
import numpy as np

from context import circuit

qubit_amount = 1

def test_XGate():
    circ = circuit.Circuit(qubit_amount)
    circ.set_gate("X", 0)
    circ.launch_circuit()
    q = circ.get_quantum_register()[0]
    assert q.get_alpha() == 0
    assert q.get_beta() == 1

def test_HGate():
    circ = circuit.Circuit(qubit_amount)
    circ.set_gate("H", 0)
    circ.launch_circuit()    
    q = circ.get_quantum_register()[0]
    print(q.get_state_vector())
    assert q.get_alpha() == 1/np.sqrt(2)
    assert q.get_beta() == 1/np.sqrt(2)