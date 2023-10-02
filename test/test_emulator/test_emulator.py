import pytest
import numpy as np

from context import circuit
from context import tools

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

def test_X_gate_with_control_index_after_target_index():
    """
    One control qubit test.
    Prepared state : |01>
    Desired output state : |11>
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 1).set_gate("X", 0, ctrl=1)
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([0, 0, 0, 1])
    assert cmp.all()
    
def test_SWAP_gate():
    """
    Prepared state : |01>
    Desired output state : |10>
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 1)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 1)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 0, 1, 0]
    assert cmp.all()
    
def test_SWAP_gate_2():
    """
    Prepared state : |10>
    Desired output state : |01>
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 0)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 1)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 1, 0, 0]
    assert cmp.all()
    
def test_SWAP_gate_3():
    """
    Test on non-adjacent qubits.
    Prepared state : |100>
    Desired outpute state : |001>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 2)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 1, 0, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_SWAP_gate_4():
    """
    Test on non-adjacent qubits.
    Prepared state : |001>
    Desired outpute state : |100>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 2)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 2)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 0, 0, 0, 1, 0, 0, 0]
    assert cmp.all()

def test_SWAP_gate_5():
    """
    Test on non-adjacent qubits.
    Prepared state : |010>
    Desired outpute state : |100>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 1)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 1)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 0, 0, 0, 1, 0, 0, 0]
    assert cmp.all()

def test_SWAP_gate_6():
    """
    Test on non-adjacent qubits.
    Prepared state : |010>
    Desired outpute state : |001>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 1)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 1, 2)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 1, 0, 0, 0, 0, 0, 0]
    assert cmp.all()

def test_SWAP_gate_7():
    """
    Test on non-adjacent qubits.
    Prepared state : |001>
    Desired outpute state : |010>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 2)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 1, 2)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 0, 1, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_SWAP_gate_8():
    """
    Test on non-adjacent qubits.
    Prepared state : |1000>
    Desired outpute state : |0001>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 3)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_SWAP_gate_9():
    """
    Test on non-adjacent qubits.
    Prepared state : |1000>
    Desired outpute state : |0100>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 1)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_SWAP_gate_9():
    """
    Test on non-adjacent qubits.
    Prepared state : |1000>
    Desired outpute state : |0010>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 2)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_SWAP_gate_9():
    """
    Test on non-adjacent qubits.
    Prepared state : |0100>
    Desired outpute state : |0001>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 1)
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 1, 3)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    
    system_matrix = circ.get_system_matrix()
    comparison = system_matrix == [pytest.approx(1/np.sqrt(2)), 0, 0, pytest.approx(1/np.sqrt(2))]

    assert comparison.all()