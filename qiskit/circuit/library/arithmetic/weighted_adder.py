# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Adds q^T * w to separate register for non-negative integer weights w
"""

import logging
from typing import List

import numpy as np

from qiskit.circuit import QuantumCircuit, QuantumRegister

logger = logging.getLogger(__name__)


class WeightedAdder(QuantumCircuit):
    """
    Adds q^T * w to separate register for non-negative integer weights w
    """

    def __init__(self, num_state_qubits: int, weights: List[int]) -> None:
        """Computes the weighted sum controlled by state qubits.

        Args:
            num_state_qubits: The number of state qubits.
            weights: The weights per state qubits.
        """

        self._weights = weights

        # check weights
        for i, weight in enumerate(weights):
            if not np.isclose(weight, np.round(weight)):
                logger.warning('Non-integer weights are rounded to '
                               'the nearest integer! (%s, %s).', i, weight)

        self._num_state_qubits = num_state_qubits
        self._num_sum_qubits = WeightedAdder.get_required_sum_qubits(weights)
        self._num_carry_qubits = self.num_sum_qubits - 1

        qr_state = QuantumRegister(self._num_state_qubits)
        qr_sum = QuantumRegister(self._num_sum_qubits)
        qr_ancilla = QuantumRegister(self.num_ancillas)

        super().__init__(qr_state, qr_sum, qr_ancilla)

        self._build(qr_state, qr_sum, qr_ancilla)

    @staticmethod
    def get_required_sum_qubits(weights):
        """ get required sum qubits """
        return int(np.floor(np.log2(sum(weights))) + 1)

    @property
    def weights(self):
        """ returns weights """
        return self._weights

    @property
    def num_state_qubits(self):
        """ returns num state qubits """
        return self._num_state_qubits

    @property
    def num_sum_qubits(self):
        """ returns num sum qubits """
        return self._num_sum_qubits

    @property
    def num_carry_qubits(self):
        """ returns num carry qubits """
        return self._num_carry_qubits

    @property
    def num_ancillas(self):
        """ required ancillas """
        if self.num_sum_qubits > 2:
            # includes one ancilla qubit for 3-controlled not gates
            # TODO: validate when the +1 is needed and make a case distinction
            return self.num_carry_qubits + 1
        else:
            return self.num_carry_qubits

    def required_ancillas_controlled(self):
        """ returns required ancillas controlled """
        return self.required_ancillas()

    def _build(self, qr_state, qr_sum, qr_ancilla):
        # set indices for sum and carry qubits (from ancilla register)
        qr_carry = qr_ancilla[:self.num_carry_qubits]
        q_control = qr_ancilla[self.num_carry_qubits]

        # loop over state qubits and corresponding weights
        for i, weight in enumerate(self.weights):
            # only act if non-trivial weight
            if weight == 0:
                continue

            # get state control qubit
            q_state = qr_state[i]

            # get bit representation of current weight
            weight_binary = '{0:b}'.format(int(weight)).rjust(self.num_sum_qubits, '0')[::-1]

            # loop over bits of current weight and add them to sum and carry registers
            for j, bit in enumerate(weight_binary):
                if bit == '1':
                    if self.num_sum_qubits == 1:
                        self.cx(q_state, qr_sum[j])
                    elif j == 0:
                        # compute (q_sum[0] + 1) into (q_sum[0], q_carry[0])
                        # - controlled by q_state[i]
                        self.ccx(q_state, qr_sum[j], qr_carry[j])
                        self.cx(q_state, qr_sum[j])
                    elif j == self.num_sum_qubits - 1:
                        # compute (q_sum[j] + q_carry[j-1] + 1) into (q_sum[j])
                        # - controlled by q_state[i] / last qubit,
                        # no carry needed by construction
                        self.cx(q_state, qr_sum[j])
                        self.ccx(q_state, qr_carry[j - 1], qr_sum[j])
                    else:
                        # compute (q_sum[j] + q_carry[j-1] + 1) into (q_sum[j], q_carry[j])
                        # - controlled by q_state[i]
                        self.x(qr_sum[j])
                        self.x(qr_carry[j - 1])
                        self.mct([q_state, qr_sum[j], qr_carry[j - 1]], qr_carry[j], [q_control])
                        self.cx(q_state, qr_carry[j])
                        self.x(qr_sum[j])
                        self.x(qr_carry[j - 1])
                        self.cx(q_state, qr_sum[j])
                        self.ccx(q_state, qr_carry[j - 1], qr_sum[j])
                else:
                    if self.num_sum_qubits == 1:
                        pass  # nothing to do, since nothing to add
                    elif j == 0:
                        pass  # nothing to do, since nothing to add
                    elif j == self.num_sum_qubits-1:
                        # compute (q_sum[j] + q_carry[j-1]) into (q_sum[j])
                        # - controlled by q_state[i] / last qubit,
                        # no carry needed by construction
                        self.ccx(q_state, qr_carry[j - 1], qr_sum[j])
                    else:
                        # compute (q_sum[j] + q_carry[j-1]) into (q_sum[j], q_carry[j])
                        # - controlled by q_state[i]
                        self.mct([q_state, qr_sum[j], qr_carry[j - 1]], qr_carry[j], [q_control])
                        self.ccx(q_state, qr_carry[j - 1], qr_sum[j])

            # uncompute carry qubits
            for j in reversed(range(len(weight_binary))):
                bit = weight_binary[j]
                if bit == '1':
                    if self.num_sum_qubits == 1:
                        pass
                    elif j == 0:
                        self.x(qr_sum[j])
                        self.ccx(q_state, qr_sum[j], qr_carry[j])
                        self.x(qr_sum[j])
                    elif j == self.num_sum_qubits - 1:
                        pass
                    else:
                        self.x(qr_carry[j - 1])
                        self.mct([q_state, qr_sum[j], qr_carry[j - 1]], qr_carry[j], [q_control])
                        self.cx(q_state, qr_carry[j])
                        self.x(qr_carry[j - 1])
                else:
                    if self.num_sum_qubits == 1:
                        pass
                    elif j == 0:
                        pass
                    elif j == self.num_sum_qubits - 1:
                        pass
                    else:
                        # compute (q_sum[j] + q_carry[j-1]) into (q_sum[j], q_carry[j])
                        # - controlled by q_state[i]
                        self.x(qr_sum[j])
                        self.mct([q_state, qr_sum[j], qr_carry[j - 1]], qr_carry[j], [q_control])
                        self.x(qr_sum[j])
