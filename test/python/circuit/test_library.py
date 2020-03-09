# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Test library of quantum circuits."""

import numpy as np
from ddt import ddt, data, unpack

from qiskit.test.base import QiskitTestCase
from qiskit import BasicAer, execute
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.library import Permutation, XOR, InnerProduct
from qiskit.circuit.library.arithmetic import LinearRotation, PolynomialRotation


class TestBooleanLogicLibrary(QiskitTestCase):
    """Test library of boolean logic quantum circuits."""

    def test_permutation(self):
        """Test permutation circuit."""
        circuit = Permutation(n_qubits=4, pattern=[1, 0, 3, 2])
        expected = QuantumCircuit(4)
        expected.swap(0, 1)
        expected.swap(2, 3)
        self.assertEqual(circuit, expected)

    def test_permutation_bad(self):
        """Test that [0,..,n-1] permutation is required (no -1 for last element)"""
        self.assertRaises(CircuitError, Permutation, 4, [1, 0, -1, 2])

    def test_xor(self):
        """Test xor circuit."""
        circuit = XOR(n_qubits=3, amount=4)
        expected = QuantumCircuit(3)
        expected.x(2)
        self.assertEqual(circuit, expected)

    def test_inner_product(self):
        """Test inner product circuit."""
        circuit = InnerProduct(n_qubits=3)
        expected = QuantumCircuit(*circuit.qregs)
        expected.cz(0, 3)
        expected.cz(1, 4)
        expected.cz(2, 5)
        self.assertEqual(circuit, expected)


@ddt
class TestArithmeticCircuits(QiskitTestCase):
    """Test the arithmetic circuits."""

    def test_linear_function(self):
        """Test the linear rotation arithmetic circuit."""
        slope, offset = 0.1, 0
        num_state_qubits = 2
        linear_rotation = LinearRotation(num_state_qubits, slope * 2, offset * 2)
        circuit = QuantumCircuit(num_state_qubits + 1)
        circuit.h(list(range(num_state_qubits)))
        circuit.append(linear_rotation.to_instruction(), list(range(num_state_qubits + 1)))

        backend = BasicAer.get_backend('statevector_simulator')
        statevector = execute(circuit, backend).result().get_statevector()

        for i, amplitude in enumerate(statevector):
            i = bin(i)[2:].zfill(num_state_qubits + 1)
            x, last_qubit = int(i[1:], 2), i[0]
            if last_qubit == '0':
                expected = np.cos(slope * x + offset) / np.sqrt(2**num_state_qubits)
            else:
                expected = np.sin(slope * x + offset) / np.sqrt(2**num_state_qubits)

            with self.subTest(x=x, last_qubit=last_qubit):
                self.assertAlmostEqual(amplitude.real, expected)
                self.assertAlmostEqual(amplitude.imag, 0)

    @data(
        ([1, 0.1], 3),
        ([0, 0.4, 2], 2),
    )
    @unpack
    def test_polynomes(self, coeffs, num_state_qubits):
        polynome = PolynomialRotation(num_state_qubits, coeffs)
        circuit = QuantumCircuit(num_state_qubits + 1 + polynome.num_ancillas)
        circuit.h(list(range(num_state_qubits)))
        circuit.append(polynome.to_instruction(), list(range(circuit.n_qubits)))

        backend = BasicAer.get_backend('statevector_simulator')
        statevector = execute(circuit, backend).result().get_statevector()

        def poly(x):
            res = 0
            for i, coeff in enumerate(coeffs):
                res += coeff * x**i
            return res

        amplitudes = {}
        for i, statevector_amplitude in enumerate(statevector):
            i = bin(i)[2:].zfill(circuit.n_qubits)[polynome.num_ancillas:]
            amplitudes[i] = amplitudes.get(i, 0) + statevector_amplitude

        for i, amplitude in amplitudes.items():
            x, last_qubit = int(i[1:], 2), i[0]
            if last_qubit == '0':
                expected = np.cos(poly(x)) / np.sqrt(2**num_state_qubits)
            else:
                expected = np.sin(poly(x)) / np.sqrt(2**num_state_qubits)

            with self.subTest(x=x, last_qubit=last_qubit):
                self.assertAlmostEqual(amplitude.real, expected)
                self.assertAlmostEqual(amplitude.imag, 0)
