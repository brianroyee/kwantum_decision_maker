from flask import Flask, render_template, request
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_quantum_answer():
    """Generate a quantum-based answer using a 2-qubit circuit."""
    try:
        # Create a quantum circuit with 2 qubits and 2 classical bits
        qc = QuantumCircuit(2, 2)
        
        # Apply quantum operations
        qc.h([0, 1])  # Apply Hadamard gates to both qubits
        qc.cx(0, 1)   # Apply CNOT gate
        theta = np.random.uniform(0, np.pi)
        qc.rx(theta, 0)  # Apply RX gate
        qc.measure([0, 1], [0, 1])  # Measure both qubits

        # Simulate the circuit
        simulator = AerSimulator()
        result = simulator.run(qc, shots=1, memory=True).result()
        outcome = result.get_memory()[0]  # Get single shot outcome

        # Define possible answers (expanded with 20 new answers distributed across 2-bit outcomes)
        answers = {
            '00': [
                "Yes (but only in this universe)",
                "Absolutely, the qubits align in your favor",
                "Definitely, the quantum gods approve",
                "Yes, with high probability amplitude",
                "Affirmative, the wavefunction agrees",
                "Certainly, the quantum state is clear"
            ],
            '01': [
                "No, unless you observe again",
                "Not quite, but a parallel universe says yes",
                "Nope, not in this quantum state",
                "No, the quantum oracle is not convinced",
                "Negative, the qubits have spoken",
                "No, but try collapsing the wavefunction again"
            ],
            '10': [
                "You are simultaneously right and wrong",
                "Schrödinger says both yes and no",
                "The answer is entangled with another question",
                "Possibly, if you entangle with the right qubits",
                "Yes and no, thanks to superposition",
                "The outcome is both true and false"
            ],
            '11': [
                "Maybe, but the universe is uncertain",
                "Quantum fluctuations suggest a maybe",
                "The universe is too uncertain to decide",
                "Perhaps, if you collapse the wavefunction differently",
                "The answer is lost in quantum noise",
                "Maybe, consult the quantum oracle again"
            ]
        }

        # Randomly select one answer from the list for the given outcome
        selected_answer = np.random.choice(answers[outcome])

        # Get circuit diagram as text
        circuit_text = qc.draw(output='text').single_string()

        # Quantum principle explanations
        explanations = {
            'superposition': "Superposition allows qubits to exist in multiple states simultaneously.",
            'entanglement': "Entanglement creates correlations between qubits.",
            'rotation': f"Rotation by {theta:.2f} radians adds quantum variability.",
            'measurement': f"Measurement collapses the state to {outcome}."
        }

        return {
            'answer': selected_answer,
            'outcome': outcome,
            'circuit': circuit_text,
            'explanations': explanations,
            'theta': f"{theta:.2f}"
        }
    except Exception as e:
        logger.error(f"Quantum computation failed: {str(e)}")
        return {
            'answer': "Quantum computation error occurred",
            'outcome': "N/A",
            'circuit': "Unable to generate circuit",
            'explanations': {},
            'theta': "N/A"
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle main page requests and form submissions."""
    result = None
    question = None
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        if question:
            result = get_quantum_answer()
        else:
            question = "Please enter a question"
    return render_template('index.html', question=question, result=result)

if __name__ == '__main__':
    # For local development only; Render uses gunicorn
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
