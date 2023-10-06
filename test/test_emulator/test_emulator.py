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
    circ.set_gate("X", 1, ctrl=[0]) # state = |11>
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
    circ.set_gate("X", 1).set_gate("X", 0, ctrl=[1])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([0, 0, 0, 1])
    assert cmp.all()
    
def test_H_gate_with_control_index_after_target_index():
    """
    One control qubit test.
    Prepared state : 1/sqrt(2) (|01> + |00>)
    Desired output state : 1/sqrt(2) (|11> + |00>)
    """
    circ = circuit.Circuit(2)
    circ.set_gate("H", 1).set_gate("X", 0, ctrl=[1])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    cmp = system_matrix == np.array([pytest.approx(1/np.sqrt(2)), 0, 0, pytest.approx(1/np.sqrt(2))])
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

def test_SWAP_gate_2_entangled():
    """
    Prepared state : 1/sqrt(2) (|00> - |11>)
    Desired output state : 1/sqrt(2) (|00> - |11>)
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 0).set_gate("H", 0).set_gate("X", 1, ctrl=[0])
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 1)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    print(result)
    cmp = result == [pytest.approx(1/np.sqrt(2)), 0, 0, pytest.approx(- 1/np.sqrt(2))]
    assert cmp.all() 

def test_SWAP_gate_3_entangled():
    """
    Prepared state : 1/sqrt(2) (|01> - |10>)
    Desired output state : 1/sqrt(2) (|10> - |01>)
    """
    circ = circuit.Circuit(2)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("H", 0).set_gate("X", 1, ctrl=[0])
    
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 1)
    
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    print(result)
    cmp = result == [0, pytest.approx(-1/np.sqrt(2)), pytest.approx(1/np.sqrt(2)), 0]
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
    
def test_SWAP_gate_10():
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

def test_SWAP_gate_11():
    """
    Test on non-adjacent qubits.
    Prepared state : |10000>
    Desired output state : |00001>
    """
    circ = circuit.Circuit(5)
    circ.set_gate("X", 0)

    circ.launch_circuit()

    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 4)

    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector

    m = np.zeros(2**5)
    m[1] = 1
    cmp = result == m
    assert cmp.all()
    
def test_SWAP_gate_12():
    """
    Test on non-adjacent qubits.
    Prepared state : |10000>
    Desired output state : |00100>
    """
    circ = circuit.Circuit(5)
    circ.set_gate("X", 0)

    circ.launch_circuit()

    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 2)

    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector

    m = np.zeros(2**5)
    m[4] = 1
    cmp = result == m
    assert cmp.all()

def test_SWAP_gate_13():
    """
    Test on non-adjacent qubits.
    Prepared state : 1/sqrt(2) (|001> + |000>)
    Desired output state : 1/sqrt(2) (|100> + |000>)
    """
    circ = circuit.Circuit(3)
    circ.set_gate("H", 2)
    circ.launch_circuit()
    
    unitary = tools.get_swap_unitary(len(circ.get_quantum_register()), 0, 2)
    state_vector = circ.get_system_matrix()
    result = unitary @ state_vector
    
    cmp = result == [pytest.approx(1/np.sqrt(2)), 0, 0, 0, pytest.approx(1/np.sqrt(2)), 0, 0, 0]
    
    assert cmp.all()

def test_Toffoli_gate_1():
    """
    Test on multi-control qubits.
    Prepared state : |110>
    Desired output state : |111>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2, ctrl=[0, 1])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 1]
    
    assert cmp.all()
    
def test_Toffoli_gate_2():
    """
    Test on multi-control qubits.
    Prepared state : |100>
    Desired output state : |100>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 2, ctrl=[0, 1])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 1, 0, 0, 0]
    
    assert cmp.all()

def test_Toffoli_gate_3():
    """
    Test on multi-control qubits.
    Prepared state : |101>
    Desired output state : |111>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 2).set_gate("X", 1, ctrl=[0, 2])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 1]
    
    assert cmp.all()

def test_Toffoli_gate_4():
    """
    Test on multi-control qubits.
    Prepared state : |011>
    Desired output state : |111>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 1).set_gate("X", 2).set_gate("X", 0, ctrl=[1, 2])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 1]
    
    assert cmp.all()

def test_Toffoli_gate_5():
    """
    Test on multi-control qubits.
    Prepared state : |001>
    Desired output state : |001>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 2).set_gate("X", 0, ctrl=[1, 2])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 1, 0, 0, 0, 0, 0, 0]
    
    assert cmp.all()

def test_Toffoli_gate_6():
    """
    Test on multi-control qubits.
    Prepared state : |000>
    Desired output state : |000>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0, ctrl=[1, 2])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [1, 0, 0, 0, 0, 0, 0, 0]
    
    assert cmp.all()

def test_Toffoli_gate_7():
    """
    Test on multi-control qubits.
    Prepared state : |111>
    Desired output state : |011>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2).set_gate("X", 0, ctrl=[1, 2])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 1, 0, 0, 0, 0]
    
    assert cmp.all()

def test_Toffoli_gate_8():
    """
    Test on multi-control qubits.
    Prepared state : |111>
    Desired output state : |101>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2).set_gate("X", 1, ctrl=[0, 2])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 1, 0, 0]
    
    assert cmp.all()
    
def test_Toffoli_gate_9():
    """
    Test on multi-control qubits.
    Prepared state : |111>
    Desired output state : |110>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2).set_gate("X", 2, ctrl=[0, 1])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 1, 0]
    
    assert cmp.all()

def test_Toffoli_gate_10():
    """
    Test on multi-control qubits.
    Prepared state : |1100>
    Desired output state : |1110>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2, ctrl=[0, 1])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    
    assert cmp.all()

def test_Toffoli_gate_11():
    """
    Test on multi-control qubits.
    Prepared state : |1100>
    Desired output state : |1110>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2, ctrl=[0, 1])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    
    assert cmp.all()

def test_Toffoli_gate_12():
    """
    Test on multi-control qubits.
    Prepared state : |1110>
    Desired output state : |1100>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2).set_gate("X", 2, ctrl=[0, 1])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    
    assert cmp.all()

def test_Toffoli_gate_12():
    """
    Test on multi-control qubits.
    Prepared state : |1001>
    Desired output state : |1101>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 3).set_gate("X", 1, ctrl=[0, 3])

    circ.launch_circuit()
    state_vector = circ.get_system_matrix()
    cmp = state_vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    
    assert cmp.all()

def test_Bell_state_plus():
    """
    Prepared state : |00>
    Desired output state : 1/sqrt(2) (|00> + |11>)
    """
    circ = circuit.Circuit(2)
    circ.set_gate("H", 0)
    circ.set_gate("X", 1, ctrl=[0])
    circ.launch_circuit()
    
    system_matrix = circ.get_system_matrix()
    comparison = system_matrix == [pytest.approx(1/np.sqrt(2)), 0, 0, pytest.approx(1/np.sqrt(2))]

    assert comparison.all()
    
def test_control_between_non_adjacent_qubits_1():
    """
    Prepared state : |001>
    Desired output state : |101>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 2).set_gate("X", 0, ctrl=[2])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 1, 0, 0]
    assert cmp.all()

def test_control_between_non_adjacent_qubits_2():
    """
    Prepared state : |100>
    Desired output state : |101>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 2, ctrl=[0])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 1, 0, 0]
    assert cmp.all()

def test_control_between_non_adjacent_qubits_3():
    """
    Prepared state : |1000>
    Desired output state : |1001>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 3, ctrl=[0])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_control_between_non_adjacent_qubits_4():
    """
    Prepared state : |1000>
    Desired output state : |1010>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 2, ctrl=[0])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_control_between_non_adjacent_qubits_5():
    """
    Prepared state : |0001>
    Desired output state : |1001>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 3).set_gate("X", 0, ctrl=[3])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    assert cmp.all()

def test_control_between_non_adjacent_qubits_5():
    """
    Prepared state : |0001>
    Desired output state : |0101>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 3).set_gate("X", 1, ctrl=[3])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert cmp.all()
    
def test_control_between_non_adjacent_qubits_6():
    """
    Prepared state : |0010>
    Desired output state : |1010>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 3).set_gate("X", 0, ctrl=[3])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    assert cmp.all()

def test_control_between_non_adjacent_qubits_7():
    """
    Prepared state : |0100>
    Desired output state : |0101>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 1).set_gate("X", 3, ctrl=[1])
    circ.launch_circuit()
    system_matrix = circ.get_system_matrix()
    
    cmp = system_matrix == [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert cmp.all()