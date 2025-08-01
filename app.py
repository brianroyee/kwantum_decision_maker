from flask import Flask, render_template, request
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

app = Flask(__name__)

def get_quantum_answer():
    #Create a quantum circuit >> 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)
    #Hadamard gates to create superposition
    qc.h(0)
    qc.h(1)
    #CNOT gate to entangle qubits
    qc.cx(0, 1)
    #RX gate with random angle for variability
    theta = np.random.uniform(0, np.pi)
    qc.rx(theta, 0)
    #Measure the qubits
    qc.measure([0, 1], [0, 1])
    #AerSimulator >> simulate circuit
    simulator = AerSimulator()
    #Run the circuit
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts(qc)
    #Measurement outcome
    outcome = list(counts.keys())[0]
    #Map outcome to an answer
    answers = {
        '00': "Yes (but only in this universe)",
        '01': "No, unless you observe again",
        '10': "You are simultaneously right and wrong",
        '11': "Maybe, but the universe is uncertain",
        
    }
    #Get text representation of the circuit
    circuit_text = qc.draw(output='text').single_string()
    #Explanations of quantum principles
    explanations = {
        'superposition': "Superposition (via Hadamard gates) puts each qubit in a state of both 0 and 1 simultaneously, creating all possible combinations.",
        'entanglement': "Entanglement (via CNOT gate) links the qubits so that the state of one depends on the other, creating a quantum correlation.",
        'rotation': f"Rotation (via RX gate with angle {theta:.2f} radians) tilts the quantum state, adding unpredictability to the outcome.",
        'measurement': f"Measurement collapses the qubits into {outcome}, determining the final answer from the quantum possibilities."
    }
    return {
        'answer': answers.get(outcome, "Quantum uncertainty prevails"),
        'outcome': outcome,
        'circuit': circuit_text,
        'explanations': explanations,
        'theta': f"{theta:.2f}"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    question = None
    if request.method == 'POST':
        question = request.form.get('question', 'No question provided')
        result = get_quantum_answer()
    return render_template('index.html', question=question, result=result)

if __name__ == '__main__':
    app.run(debug=True)