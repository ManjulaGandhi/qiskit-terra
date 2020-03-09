# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Polynomially controlled Pauli-rotations."""

from typing import List

from itertools import product
from sympy.ntheory.multinomial import multinomial_coefficients
import numpy as np

from qiskit.circuit import QuantumCircuit, QuantumRegister


class PolynomialRotation(QuantumCircuit):
    r"""
    Polynomial rotation.

    For a polynomial :math`p(x)`, a basis state :math:`|i\rangle` and a target qubit
    :math:`|0\rangle` this operator acts as:

    .. math::

        |i\rangle |0\rangle \mapsto \cos(p(i)) |i\rangle |0\rangle + \sin(p(i)) |i\rangle |1\rangle

    Let n be the number of qubits representing the state, d the degree of p(x) and q_i the qubits,
    where q_0 is the least significant qubit. Then for

    .. math::

        x = \sum_{i=0}^{n-1} 2^i q_i,

    we can write

    .. math::

        p(x) = \sum_{j=0}^{j=d} c_j x_j

    where :math:`c` are the input coefficients, ``coeffs``.
    """

    def __init__(self, num_state_qubits: int, coeffs: List[float], basis: str = 'Y',
                 reverse: bool = False):
        """Prepare an approximation to a state with amplitudes specified by a polynomial.

        Args:
            num_state_qubits: The number of qubits representing the state.
            coeffs: The coefficients of the polynomial. ``coeffs[i]`` is the coefficient of the
                i-th power of x.
            basis: The type of Pauli rotation ('X', 'Y', 'Z').
            reverse: If True, apply the polynomial with the reversed list of qubits
                (i.e. q_n as q_0, q_n-1 as q_1, etc).

        Raises:
            ValueError: invalid input
        """
        # store parameters
        self.num_state_qubits = num_state_qubits
        self.coeffs = coeffs
        self.degree = len(coeffs) - 1
        self.basis = basis.lower()
        self.reverse = reverse

        if self.basis not in ['x', 'y', 'z']:
            raise ValueError('The provided basis must be X, Y or Z, not {}'.format(basis))

        qr_state = QuantumRegister(num_state_qubits)
        qr_target = QuantumRegister(1)
        qr_ancilla = QuantumRegister(self.num_ancillas)  # based on self.degree
        super().__init__(qr_state, qr_target, qr_ancilla)

        self._build(qr_state, qr_target, qr_ancilla)

    @property
    def num_ancillas(self):
        return max(1, self.degree - 1)

    @property
    def num_ancillas_controlled(self):
        return max(1, self.degree)

    def _get_controls(self):
        """
        The list of controls is the list of all
        monomials of the polynomial, where the qubits are the variables.
        """
        t = [0] * (self.num_state_qubits - 1) + [1]
        cdict = {tuple(t): 0}
        clist = list(product([0, 1], repeat=self.num_state_qubits))
        index = 0
        while index < len(clist):
            tsum = 0
            i = clist[index]
            for j in i:
                tsum = tsum + j
            if tsum > self.degree:
                clist.remove(i)
            else:
                index = index + 1
        clist.remove(tuple([0] * self.num_state_qubits))
        # For now set all angles to 0
        for i in clist:
            cdict[i] = 0
        return cdict

    def _get_thetas(self, cdict):
        """
        Compute the coefficient of each monomial.
        This will be the argument for the controlled y-rotation.
        """
        for j in range(1, len(self.coeffs)):
            # List of multinomial coefficients
            mlist = multinomial_coefficients(self.num_state_qubits, j)
            # Add angles
            for m in mlist:
                temp_t = []
                powers = 1
                # Get controls
                for k in range(0, len(m)):  # pylint: disable=consider-using-enumerate
                    if m[k] > 0:
                        temp_t.append(1)
                        powers *= 2 ** (k * m[k])
                    else:
                        temp_t.append(0)
                temp_t = tuple(temp_t)
                # Add angle
                cdict[temp_t] += self.coeffs[j] * mlist[m] * powers
        return cdict

    def _build(self, qr_state, qr_target, qr_ancilla):
        # dictionary of controls for the rotation gates as a tuple and their respective angles
        cdict = self._get_thetas(self._get_controls())

        if self.basis == 'x':
            self.rx(2 * self.coeffs[0], qr_target)
        elif self.basis == 'y':
            self.ry(2 * self.coeffs[0], qr_target)
        else:
            self.rz(2 * self.coeffs[0], qr_target)

        for c in cdict:
            qr_control = []
            if self.reverse:
                for i, _ in enumerate(c):
                    if c[i] > 0:
                        qr_control.append(qr_state[qr_state.size - i - 1])
            else:
                for i, _ in enumerate(c):
                    if c[i] > 0:
                        qr_control.append(qr_state[i])

            # apply controlled rotations
            if len(qr_control) > 1:
                if self.basis == 'x':
                    self.mcrx(2 * cdict[c], qr_control, qr_target[0], qr_ancilla)
                elif self.basis == 'y':
                    self.mcry(2 * cdict[c], qr_control, qr_target[0], qr_ancilla)
                else:
                    self.mcrz(2 * cdict[c], qr_control, qr_target[0], qr_ancilla)

            elif len(qr_control) == 1:
                if self.basis == 'x':
                    self.u3(2 * cdict[c], -np.pi / 2, np.pi / 2, qr_control[0], qr_target)
                elif self.basis == 'y':
                    self.cry(2 * cdict[c], qr_control[0], qr_target[0])
                else:
                    self.crz(2 * cdict[c], qr_control[0], qr_target[0])
