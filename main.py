from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.visualization import plot_histogram
import numpy as np

def create_string_vibration_circuit(num_qubits=4, num_dimensions=2):
    """
    Creates a quantum circuit that simulates simplified string vibrations in multiple dimensions.
    
    Args:
        num_qubits (int): Number of qubits to represent each spatial point on the string
        num_dimensions (int): Number of spatial dimensions to simulate (2 or 3)
    
    Returns:
        QuantumCircuit: The quantum circuit representing string vibrations
    """
    # Create quantum and classical registers
    qr = QuantumRegister(num_qubits * num_dimensions, 'string')
    cr = ClassicalRegister(num_qubits * num_dimensions, 'measurement')
    circuit = QuantumCircuit(qr, cr)
    
    # Initialize superposition states to represent possible vibration modes
    for i in range(num_qubits * num_dimensions):
        circuit.h(i)
    
    # Entangle neighboring points to simulate string tension
    for dim in range(num_dimensions):
        for i in range(num_qubits - 1):
            control = i + (dim * num_qubits)
            target = (i + 1) + (dim * num_qubits)
            circuit.cx(control, target)
    
    # Add phase rotations to simulate energy levels
    for i in range(num_qubits * num_dimensions):
        circuit.rz(np.pi / 4, i)
    
    # Create interference between dimensions
    if num_dimensions > 1:
        for i in range(num_qubits):
            for dim1 in range(num_dimensions):
                for dim2 in range(dim1 + 1, num_dimensions):
                    control = i + (dim1 * num_qubits)
                    target = i + (dim2 * num_qubits)
                    circuit.cz(control, target)
    
    # Measure all qubits
    circuit.measure(qr, cr)
    
    return circuit

def simulate_string_theory():
    """
    Performs the string theory simulation and returns results.
    
    Returns:
        dict: Measurement results and their counts
    """
    # Create circuit with 4 qubits per dimension
    circuit = create_string_vibration_circuit(num_qubits=4, num_dimensions=2)
    
    # Run on quantum simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1000)
    result = job.result()
    
    return result.get_counts(circuit)

def analyze_results(counts):
    """
    Analyzes the simulation results.
    
    Args:
        counts (dict): Measurement results and their counts
        
    Returns:
        dict: Analysis of the results
    """
    total_shots = sum(counts.values())
    analysis = {
        'total_measurements': total_shots,
        'unique_states': len(counts),
        'most_common_state': max(counts.items(), key=lambda x: x[1])[0],
        'highest_probability': max(counts.values()) / total_shots
    }
    return analysis

# Example usage
def run_simulation():
    """
    Runs the complete simulation and prints analysis.
    """
    print("Running string theory simulation...")
    counts = simulate_string_theory()
    analysis = analyze_results(counts)
    
    print("\nSimulation Results:")
    print(f"Total measurements: {analysis['total_measurements']}")
    print(f"Unique states observed: {analysis['unique_states']}")
    print(f"Most common state: {analysis['most_common_state']}")
    print(f"Highest probability: {analysis['highest_probability']:.4f}")
    
    return counts, analysis
