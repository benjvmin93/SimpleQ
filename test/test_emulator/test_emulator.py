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
    q = circ.get_quantum_register()[0]
    assert q.get_alpha() == 0 and q.get_beta() == 1

def test_H_gate():
    """
    Hadamard gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("H", 0)
    circ.launch_circuit()    
    q = circ.get_quantum_register()[0]
    expected_value = 1 / np.sqrt(2)
    assert q.get_alpha() == pytest.approx(expected_value) and q.get_beta() == pytest.approx(expected_value)
    
def test_Y_gate():
    """
    Y gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("Y", 0)
    circ.launch_circuit()
    q = circ.get_quantum_register()[0]
    assert q.get_alpha() == 0 and q.get_beta() == 1j

def test_Z_gate():
    """
    Z gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("X", 0).set_gate("Z", 0)
    circ.launch_circuit()
    q = circ.get_quantum_register()[0]
    assert q.get_alpha() == 0 and q.get_beta() == -1
    
def test_gate_with_one_control():
    """
    One control qubit test.
    Prepared state : |10>
    Desired output state : |11>
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 0)   # state = |10>
    circ.set_gate("X", 1, ctrl=0) # state = |11>
    circ.launch_circuit()
    q = circ.get_quantum_register()
    q0, q1 = q[0], q[1]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 0 and q1.get_beta() == 1

def test_Toffoli_gate_1():
    """
    Toffoli gate test.
    Prepared state : |000>
    Desired output state : |000>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 2, ctrl=0).set_gate("X", 2, ctrl=1).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2 = q[0], q[1], q[2]
    assert q0.get_alpha() == 1 and q0.get_beta() == 0
    assert q1.get_alpha() == 1 and q1.get_beta() == 0
    assert q2.get_alpha() == 1 and q2.get_beta() == 0
    
def test_Toffoli_gate_2():
    """
    Toffoli gate test.
    Prepared state : |110>
    Desired output state : |111>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2, ctrl=0).set_gate("X", 2, ctrl=1).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2 = q[0], q[1], q[2]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 0 and q1.get_beta() == 1
    assert q2.get_alpha() == 0 and q2.get_beta() == 1

"""
    The toffoli gate tests require the implementation of multicontrol gate.

def test_Toffoli_gate_3():
    
    Toffoli gate test.
    Prepared state : |111>
    Desired output state : |110>
    
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2).set_gate("X", 2, ctrl=0).set_gate("X", 2, ctrl=1).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2 = q[0], q[1], q[2]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 0 and q1.get_beta() == 1
    assert q2.get_alpha() == 1 and q2.get_beta() == 0
    
def test_Toffoli_gate_4():
    
    Toffoli gate test.
    Prepared state : |1010>
    Desired output state : |1011>
    
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 2).set_gate("X", 3, ctrl=0).set_gate("X", 3, ctrl=2).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2, q3 = q[0], q[1], q[2], q[3]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 1 and q1.get_beta() == 0
    assert q2.get_alpha() == 0 and q2.get_beta() == 1
    assert q3.get_alpha() == 0 and q3.get_beta() == 1
"""