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
from qiskit.circuit.library.arithmetic import (LinearRotation, PolynomialRotation,
                                               FixedValueComparator, PiecewiseLinearRotation)


class TestBooleanLogicLibrary(QiskitTestCase):
    """Test library of boolean logic quantum circuits."""

    def test_permutation(self):
        """Test permutation circuit."""
        circuit = Permutation(num_qubits=4, pattern=[1, 0, 3, 2])
        expected = QuantumCircuit(4)
        expected.swap(0, 1)
        expected.swap(2, 3)
        self.assertEqual(circuit, expected)

    def test_permutation_bad(self):
        """Test that [0,..,n-1] permutation is required (no -1 for last element)"""
        self.assertRaises(CircuitError, Permutation, 4, [1, 0, -1, 2])

    def test_xor(self):
        """Test xor circuit."""
        circuit = XOR(num_qubits=3, amount=4)
        expected = QuantumCircuit(3)
        expected.x(2)
        self.assertEqual(circuit, expected)

    def test_inner_product(self):
        """Test inner product circuit."""
        circuit = InnerProduct(num_qubits=3)
        expected = QuantumCircuit(*circuit.qregs)
        expected.cz(0, 3)
        expected.cz(1, 4)
        expected.cz(2, 5)
        self.assertEqual(circuit, expected)


@ddt
class TestLinearRotation(QiskitTestCase):
    """Test the arithmetic circuits."""

    def test_linear_function(self):
        """Test the linear rotation arithmetic circuit."""
        slope, offset = 0.1, 0
        num_state_qubits = 2
        linear_rotation = LinearRotation(num_state_qubits + 1, slope * 2, offset * 2)
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


@ddt
class TestPolynomialRotation(QiskitTestCase):
    """Test the arithmetic circuits."""
    @data(
        ([1, 0.1], 3),
        ([0, 0.4, 2], 2),
    )
    @unpack
    def test_polynomes(self, coeffs, num_state_qubits):
        """Test the polynomial rotation."""
        polynome = PolynomialRotation(num_state_qubits, coeffs)
        circuit = QuantumCircuit(num_state_qubits + 1 + polynome.num_ancillas)
        circuit.h(list(range(num_state_qubits)))
        circuit.append(polynome.to_instruction(), list(range(circuit.num_qubits)))

        backend = BasicAer.get_backend('statevector_simulator')
        statevector = execute(circuit, backend).result().get_statevector()

        def poly(x):
            res = sum(coeff * x**i for i, coeff in enumerate(coeffs))
            return res

        amplitudes = {}
        for i, statevector_amplitude in enumerate(statevector):
            i = bin(i)[2:].zfill(circuit.num_qubits)[polynome.num_ancillas:]
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


@ddt
class TestPiecewiseLinearRotation(QiskitTestCase):
    """Test the arithmetic circuits."""
    @data(
        (3, [1, 3], [1, 0, -0.5], [0, 0, 0])
    )
    @unpack
    def test_piecewise_linear(self, num_state_qubits, breakpoints, slopes, offsets):
        """Test the piecewise linear rotations."""
        pw_linear_function = PiecewiseLinearRotation(num_state_qubits, breakpoints,
                                                     [2 * slope for slope in slopes],
                                                     [2 * offset for offset in offsets])

        def reference(x):
            for i, point in enumerate(breakpoints[1:] + [2**num_state_qubits]):
                if x >= point:
                    return offsets[-i] + slopes[-i] * (x - point)
            return 0

        circuit = QuantumCircuit(num_state_qubits + 1 + pw_linear_function.num_ancillas)
        circuit.h(list(range(num_state_qubits)))
        circuit.append(pw_linear_function.to_gate(), list(range(circuit.num_qubits)))

        import matplotlib.pyplot as plt
        circuit.decompose().draw(output='mpl')
        plt.show()

        backend = BasicAer.get_backend('statevector_simulator')
        statevector = execute(circuit, backend).result().get_statevector()

        amplitudes = {}
        for i, statevector_amplitude in enumerate(statevector):
            # print('ancillas', pw_linear_function.num_ancillas, 'num', circuit.num_qubits)
            # print('before', i)
            i = bin(i)[2:].zfill(circuit.num_qubits)[pw_linear_function.num_ancillas:]
            # print('after', i)
            amplitudes[i] = amplitudes.get(i, 0) + statevector_amplitude
            # print()

        for i, amplitude in amplitudes.items():
            x, last_qubit = int(i[1:], 2), i[0]
            if last_qubit == '0':
                expected = np.cos(reference(x)) / np.sqrt(2**num_state_qubits)
            else:
                expected = np.sin(reference(x)) / np.sqrt(2**num_state_qubits)

            print('x', x, 'calculated', amplitude.real, 'expected', expected)
            with self.subTest(x=x, last_qubit=last_qubit):
                self.assertAlmostEqual(amplitude.real, expected)
                self.assertAlmostEqual(amplitude.imag, 0)


@ddt
class TestFixedValueComparator(QiskitTestCase):
    """Text Fixed Value Comparator"""

    def assertComparisonIsCorrect(self, comp, num_state_qubits, value, geq):
        """Assert that the comparator output is correct."""
        qc = QuantumCircuit(comp.n_qubits)  # initialize circuit
        qc.h(list(range(num_state_qubits)))  # set equal superposition state
        qc.append(comp, list(range(comp.n_qubits)))  # add comparator

        # run simulation
        backend = BasicAer.get_backend('statevector_simulator')
        statevector = execute(qc, backend).result().get_statevector()
        for i, amplitude in enumerate(statevector):
            prob = np.abs(amplitude)**2
            if prob > 1e-6:
                # equal superposition
                self.assertEqual(True, np.isclose(1.0, prob * 2.0**num_state_qubits))
                b_value = '{0:b}'.format(i).rjust(qc.width(), '0')
                x = int(b_value[(-num_state_qubits):], 2)
                comp_result = int(b_value[-num_state_qubits-1], 2)
                if geq:
                    self.assertEqual(x >= value, comp_result == 1)
                else:
                    self.assertEqual(x < value, comp_result == 1)

    @data(
        # n, value, geq
        [1, 0, True],
        [1, 1, True],
        [2, -1, True],
        [3, 5, True],
        [3, 2, True],
        [3, 2, False],
        [4, 6, False]
    )
    @unpack
    def test_fixed_value_comparator(self, num_state_qubits, value, geq):
        """Test the fixed value comparator circuit."""
        # build the circuit with the comparator
        comp = FixedValueComparator(num_state_qubits, value, geq=geq)
        self.assertComparisonIsCorrect(comp, num_state_qubits, value, geq)

    def test_mutability(self):
        """Test changing the arguments of the comparator."""

        comp = FixedValueComparator()

        with self.subTest(msg='missing num state qubits and value'):
            with self.assertRaises(AttributeError):
                print(comp.draw())

        comp.num_state_qubits = 2

        with self.subTest(msg='missing value'):
            with self.assertRaises(AttributeError):
                print(comp.draw())

        comp.value = 0
        comp.geq = True

        with self.subTest(msg='updating num state qubits'):
            comp.num_state_qubits = 1
            self.assertComparisonIsCorrect(comp, 1, 0, True)

        with self.subTest(msg='updating the value'):
            comp.num_state_qubits = 3
            comp.value = 2
            self.assertComparisonIsCorrect(comp, 3, 2, True)

        with self.subTest(msg='updating geq'):
            comp.geq = False
            self.assertComparisonIsCorrect(comp, 3, 2, False)
