import pytest
import numpy as np

from context import circuit

def test_X_gate():
    """
    X gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("X", 0)
    circ.launch_circuit()
    
    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([0, 1])
    assert cmp.all()

def test_H_gate():
    """
    Hadamard gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("H", 0)
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    expected_value = 1 / np.sqrt(2)
    cmp = system_matrix == np.array([pytest.approx(expected_value), pytest.approx(expected_value)])
    assert cmp.all()
    
def test_Y_gate():
    """
    Y gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("Y", 0)
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([0, 1j])
    assert cmp.all()

def test_Z_gate():
    """
    Z gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("X", 0).set_gate("Z", 0)
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([0, -1])
    assert cmp.all()
    
def test_X_gate_with_one_control():
    """
    One control qubit test.
    Prepared state : |10>
    Desired output state : |11>
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 0)   # state = |10>
    circ.set_gate("X", 1, ctrl=0) # state = |11>
    circ.launch_circuit()

    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([0, 0, 0, 1])
    assert cmp.all()

def test_Bell_state_plus():
    """
    Prepared state : |00>
    Desired output state : 1/sqrt(2) (|00> + |11>)
    """
    circ = circuit.Circuit(2)
    circ.set_gate("H", 0)
    circ.set_gate("X", 1, ctrl=0)
    circ.launch_circuit()
    q = circ.get_quantum_register()
    q0, q1 = q[0], q[1]
    
    system_matrix = circ.get_system_matrix()
    comparison = system_matrix == [pytest.approx(1/np.sqrt(2)), 0, 0, pytest.approx(1/np.sqrt(2))]

    assert comparison.all()