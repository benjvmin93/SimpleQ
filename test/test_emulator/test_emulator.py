import numpy as np

from src.QLibrary.SimpleQ import circuit


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
    assert q.get_alpha() == 1/np.sqrt(2) and q.get_beta() == 1/np.sqrt(2)
    
def test_Y_gate():
    """
    Y gate test.
    """
    circ = circuit.Circuit(1)
    circ.set_gate("Y", 0)
    circ.launch_circuit()
    q = circ.get_quantum_register()[0]
    assert q.get_alpha() == 0 and q.get_beta() == -1j

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
    circ.set_gate("X", 1, ctrl=[0]) # state = |11>
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
    circ.set_gate("X", 2, ctrl=[0, 1]).launch_circuit()
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
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2, ctrl=[0, 1]).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2 = q[0], q[1], q[2]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 0 and q1.get_beta() == 1
    assert q2.get_alpha() == 0 and q2.get_beta() == 1

def test_Toffoli_gate_3():
    """
    Toffoli gate test.
    Prepared state : |111>
    Desired output state : |110>
    """
    circ = circuit.Circuit(3)
    circ.set_gate("X", 0).set_gate("X", 1).set_gate("X", 2).set_gate("X", 2, ctrl=[0, 1]).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2 = q[0], q[1], q[2]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 0 and q1.get_beta() == 1
    assert q2.get_alpha() == 1 and q2.get_beta() == 0
    
def test_Toffoli_gate_4():
    """
    Toffoli gate test.
    Prepared state : |1010>
    Desired output state : |1011>
    """
    circ = circuit.Circuit(4)
    circ.set_gate("X", 0).set_gate("X", 2).set_gate("X", 3, ctrl=[0, 2]).launch_circuit()
    q = circ.get_quantum_register()
    q0, q1, q2, q3 = q[0], q[1], q[2], q[3]
    assert q0.get_alpha() == 0 and q0.get_beta() == 1
    assert q1.get_alpha() == 1 and q1.get_beta() == 0
    assert q2.get_alpha() == 0 and q2.get_beta() == 1
    assert q3.get_alpha() == 0 and q3.get_beta() == 1

class Gate_Model:
    def __init__(self, index, name, ctrl):
        self.model = {
            "index": index,
            "name": name,
            "ctrl": ctrl
        }
    
    def get_model(self):
        return self.model
    
def prepare_model(index, name, ctrl):
    return Gate_Model(index, name, ctrl).get_model()

def test_custom_gate_1():
    """
    Custom gate test.
    Double X on 1 qubit.
    Prepared gate : X-X
    Prepared state : |0>
    Desired output state : |0>
    """
    
    model = prepare_model(0, "X", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 1,
        "BLOCKS": [model, model],
    }
    
    circ = circuit.Circuit(1)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    cmp = m == [1, 0]
    assert cmp.all() == True

def test_custom_gate_2():
    """
    Custom gate test.
    Double X on 1 qubit.
    Prepared gate : X
    Prepared state : |0>
    Desired output state : |1>
    """
    
    model = prepare_model(0, "X", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 1,
        "BLOCKS": [model],
    }
    
    circ = circuit.Circuit(1)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    cmp = m == [0, 1]
    assert cmp.all() == True

def test_custom_gate_3():
    """
    Custom gate test.
    X on 2 qubit.
    Prepared gate : 
        |0> -X-
        |0> -X-
    Prepared state : |00>
    Desired output state : |11>
    """
    
    model_1 = prepare_model(0, "X", None)
    model_2 = prepare_model(1, "X", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 2,
        "BLOCKS": [model_1, model_2],
    }
    
    circ = circuit.Circuit(2)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    cmp = m == [0, 0, 0, 1]
    assert cmp.all() == True
    
def test_custom_gate_4():
    """
    Custom gate test.
    X on 1 qubit.
    Prepared gate : 
        |0> -X-
        |0> ---
    Prepared state : |00>
    Desired output state : |10>
    """
    
    model_1 = prepare_model(0, "X", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 1,
        "BLOCKS": [model_1],
    }
    
    circ = circuit.Circuit(2)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    cmp = m == [0, 0, 1, 0]
    assert cmp.all() == True
    
def test_custom_gate_5():
    """
    Custom gate test.
    Prepared gate : 
        |0> -X-X-X
        |0> -X----
    Prepared state : |00>
    Desired output state : |11>
    """
    
    model_1 = prepare_model(0, "X", None)
    model_2 = prepare_model(1, "X", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 1,
        "BLOCKS": [model_1, model_1, model_1, model_2],
    }
    
    circ = circuit.Circuit(2)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    cmp = m == [0, 0, 0, 1]
    assert cmp.all() == True
    
def test_custom_gate_6():
    """
    Custom gate test.
    Same test as test_custom_gate_5() but we change the position of model_2 in the blocks list. It shouldn't change anything
    Prepared gate : 
        |0> -X-X-X
        |0> -X----
    Prepared state : |00>
    Desired output state : |11>
    """
    
    model_1 = prepare_model(0, "X", None)
    model_2 = prepare_model(1, "X", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 1,
        "BLOCKS": [model_1, model_2, model_1, model_1],
    }
    
    circ = circuit.Circuit(2)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    cmp = m == [0, 0, 0, 1]
    assert cmp.all() == True
    
def test_custom_gate_7():
    """
    Custom gate test.
    Prepared gate : 
        |0> -H-
        |0> -H-
    Prepared state : |00>
    Desired output state : 1/sqrt(4) (|00> + |01> + |10> + |11>)
    """
    
    model_1 = prepare_model(0, "H", None)
    model_2 = prepare_model(1, "H", None)
    
    gate_model = {
        "NAME": "test",
        "QUBITS": 1,
        "BLOCKS": [model_1, model_2],
    }
    
    circ = circuit.Circuit(2)
    gate = circ.create_gate(gate_model)
    system = circ.get_system_matrix()
    m = np.array(np.dot(gate["matrix"], system))
    norm = np.sqrt(np.abs(np.sum(m)) ** 2) # don't forget to normalize
    m /= norm
    cmp = m == [1/4, 1/4, 1/4, 1/4]
    assert cmp.all() == True