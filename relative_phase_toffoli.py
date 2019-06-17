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
Relative Phase Toffoli Gates.
"""

from qiskit.circuit import QuantumCircuit, Qubit
from qiskit.qasm import pi

from qiskit.aqua import AquaError


def _apply_rccx(circ, a, b, c):
    circ.u2(0, pi, c)  # h
    circ.u1(pi / 4, c)  # t
    circ.cx(b, c)
    circ.u1(-pi / 4, c)  # tdg
    circ.cx(a, c)
    circ.u1(pi / 4, c)  # t
    circ.cx(b, c)
    circ.u1(-pi / 4, c)  # tdg
    circ.u2(0, pi, c)  # h


def _apply_rcccx(circ, a, b, c, d):
    circ.u2(0, pi, d)  # h
    circ.u1(pi / 4, d)  # t
    circ.cx(c, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.u2(0, pi, d)  # h
    circ.cx(a, d)
    circ.u1(pi / 4, d)  # t
    circ.cx(b, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.cx(a, d)
    circ.u1(pi / 4, d)  # t
    circ.cx(b, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.u2(0, pi, d)  # h
    circ.u1(pi / 4, d)  # t
    circ.cx(c, d)
    circ.u1(-pi / 4, d)  # tdg
    circ.u2(0, pi, d)  # h


def rccx(self, q_control_1, q_control_2, q_target):
    """
    Apply 2-Control Relative-Phase Toffoli gate from q_control_1 and q_control_2 to q_target.

    The implementation is based on https://arxiv.org/pdf/1508.03273.pdf Figure 3

    Args:
        self (QuantumCircuit): The QuantumCircuit object to apply the rccx gate on.
        q_control_1 (Qubit): The 1st control qubit.
        q_control_2 (Qubit): The 2nd control qubit.
        q_target (Qubit): The target qubit.

    """
    if not isinstance(q_control_1, Qubit):
        raise AquaError('A qubit is expected for the first control.')
    if not self.has_register(q_control_1.register):
        raise AquaError('The first control qubit is expected to be part of the circuit.')

    if not isinstance(q_control_2, Qubit):
        raise AquaError('A qubit is expected for the second control.')
    if not self.has_register(q_control_2.register):
        raise AquaError('The second control qubit is expected to be part of the circuit.')

    if not isinstance(q_target, Qubit):
        raise AquaError('A qubit is expected for the target.')
    if not self.has_register(q_target.register):
        raise AquaError('The target qubit is expected to be part of the circuit.')
    self._check_dups([q_control_1, q_control_2, q_target])
    _apply_rccx(self, q_control_1, q_control_2, q_target)


def rcccx(self, q_control_1, q_control_2, q_control_3, q_target):
    """
    Apply 3-Control Relative-Phase Toffoli gate from q_control_1, q_control_2, and q_control_3 to q_target.

    The implementation is based on https://arxiv.org/pdf/1508.03273.pdf Figure 4

    Args:
        self (QuantumCircuit): The QuantumCircuit object to apply the rcccx gate on.
        q_control_1 (Qubit): The 1st control qubit.
        q_control_2 (Qubit): The 2nd control qubit.
        q_control_3 (Qubit): The 3rd control qubit.
        q_target (Qubit): The target qubit.

    """
    if not isinstance(q_control_1, Qubit):
        raise AquaError('A qubit is expected for the first control.')
    if not self.has_register(q_control_1.register):
        raise AquaError('The first control qubit is expected to be part of the circuit.')

    if not isinstance(q_control_2, Qubit):
        raise AquaError('A qubit is expected for the second control.')
    if not self.has_register(q_control_2.register):
        raise AquaError('The second control qubit is expected to be part of the circuit.')

    if not isinstance(q_control_3, Qubit):
        raise AquaError('A qubit is expected for the third control.')
    if not self.has_register(q_control_3.register):
        raise AquaError('The third control qubit is expected to be part of the circuit.')

    if not isinstance(q_target, Qubit):
        raise AquaError('A qubit is expected for the target.')
    if not self.has_register(q_target.register):
        raise AquaError('The target qubit is expected to be part of the circuit.')

    self._check_dups([q_control_1, q_control_2, q_control_3, q_target])
    _apply_rcccx(self, q_control_1, q_control_2, q_control_3, q_target)


QuantumCircuit.rccx = rccx
QuantumCircuit.rcccx = rcccx
