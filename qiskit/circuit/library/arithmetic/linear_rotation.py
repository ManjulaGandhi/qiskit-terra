# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Linearly-controlled X, Y or Z rotation."""

import numpy as np

from qiskit.circuit import QuantumCircuit, QuantumRegister


class LinearRotation(QuantumCircuit):
    r"""Linearly-controlled X, Y or Z rotation.

    For a register of state qubits |x>, a target qubit |0> and the basis 'Y' this
    circuit acts as:

    q_0:     |0>─────────────────────────■───────── ... ──────────────────────
                                         │
                                         .
                                         │
    q_(n-1): |0>─────────────────────────┼───────── ... ───────────■──────────
                 ┌────────────┐  ┌───────┴───────┐       ┌─────────┴─────────┐
    q_n:     |0>─┤ RY(offset) ├──┤ RY(2^0 slope) ├  ...  ┤ RY(2^(n-1) slope) ├
                 └────────────┘  └───────────────┘       └───────────────────┘

    This can for example be used to approximate linear functions, with :math:`a/2` = slope
    and :math:`b/2` = offset and the basis 'Y':

    .. math::

        |x\rangle |0\rangle \mapsto \cos(ax + b)|x\rangle|0\rangle + \sin(ax + b)|x\rangle |1\rangle

    Since for small arguments :math:`\sin(x) \approx x` this operator can be used to approximate
    linear functions.

    """

    def __init__(self, num_state_qubits: int, slope: float, offset: float, basis: str = 'Y'
                 ) -> None:
        r"""
        Args:
            num_state_qubits (int): The number of qubits representing the state :math:`|x\rangle`.
            slope (float): The slope of the controlled rotation.
            offset (float): The offset of the controlled rotation.
            basis (str): The type of Pauli rotation ('X', 'Y', 'Z').

        Raises:
            ValueError: invalid input
        """
        qr_state = QuantumRegister(num_state_qubits, name='state')
        qr_target = QuantumRegister(1, name='target')
        super().__init__(qr_state, qr_target)

        # store parameters
        self.num_control_qubits = num_state_qubits
        self.slope = slope
        self.offset = offset
        self.basis = basis.lower()

        if self.basis not in ['x', 'y', 'z']:
            raise ValueError('The provided basis must be X, Y or Z, not {}'.format(basis))

        self._build(qr_state, qr_target)

    def _build(self, qr_state, qr_target):
        if not np.isclose(self.offset / 4 / np.pi % 1, 0):
            if self.basis == 'x':
                self.rx(self.offset, qr_target)
            elif self.basis == 'y':
                self.ry(self.offset, qr_target)
            else:  # 'Z':
                self.rz(self.offset, qr_target)
        for i, q_i in enumerate(qr_state):
            theta = self.slope * pow(2, i)
            if not np.isclose(theta / 4 / np.pi % 1, 0):
                if self.basis == 'x':
                    self.crx(self.slope * pow(2, i), q_i, qr_target)
                elif self.basis == 'y':
                    self.cry(self.slope * pow(2, i), q_i, qr_target)
                else:  # 'Z'
                    self.crz(self.slope * pow(2, i), q_i, qr_target)
