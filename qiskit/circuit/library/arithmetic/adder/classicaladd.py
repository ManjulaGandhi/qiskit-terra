# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals

"""Module-level docstring describing what the file content is."""

from qiskit.circuit import QuantumCircuit, QuantumRegister


class ClassicalAdd(QuantumCircuit):
    """To implement Classical Addtion in QFT Adder paper.

    Based on the information given in [1].

    **References**

    [1] Thomas G.Draper, 2000. "Addition on a Quantum Computer"
    `Journal https://arxiv.org/pdf/quant-ph/0008033.pdf`_
    """

    def __init__(self, num_state_qubits: int, name: str = 'ClassicalAdd') -> None:
        """
        Args:
            num_state_qubits: The size of the register.
            name: The name of the circuit.
        """
        # define the registers
        qr_a = QuantumRegister(num_state_qubits, name='a')
        qr_b = QuantumRegister(num_state_qubits, name='b')
        qr_cin = QuantumRegister(num_state_qubits, name='cin')
        qr_cout = QuantumRegister(1, name='cout')

        # initialize the circuit
        super().__init__(qr_a, qr_b, qr_cin, qr_cout, name=name)

        qc_carry = QuantumCircuit(4, name='Carry')
        qc_carry.ccx(1, 2, 3)
        qc_carry.cx(1, 2)
        qc_carry.ccx(0, 2, 3)
        qc_instruction_carry = qc_carry.to_instruction()

        qc_sum = QuantumCircuit(3, name='Sum')
        qc_sum.cx(1, 2)
        qc_sum.cx(0, 2)
        qc_instruction_sum = qc_sum.to_instruction()

        # Build a temporary subcircuit that adds a to b,
        # storing the result in b

        for j in range(num_state_qubits - 1):
            self.append(qc_instruction_carry, [qr_cin[j], qr_a[j], qr_b[j], qr_cin[j+1]])

        self.append(qc_instruction_carry, [qr_cin[num_state_qubits - 1],
                                           qr_a[num_state_qubits - 1], qr_b[num_state_qubits - 1],
                                           qr_cout])
        self.cx(qr_a[num_state_qubits - 1], qr_b[num_state_qubits - 1])
        self.append(qc_instruction_sum, [qr_cin[num_state_qubits - 1],
                                         qr_a[num_state_qubits - 1], qr_b[num_state_qubits - 1]])

        for j in reversed(range(num_state_qubits - 1)):
            self.append(qc_instruction_carry, [qr_cin[j], qr_a[j], qr_b[j], qr_cin[j+1]])
            self.append(qc_instruction_sum, [qr_cin[j], qr_a[j], qr_b[j]])
