# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Linearly-controlled X, Y or Z rotation."""

from typing import Optional, List, Tuple
import numpy as np

from qiskit.circuit import QuantumCircuit, QuantumRegister, Qubit, Clbit, Instruction


class LinearPauliRotations(QuantumCircuit):
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

    def __init__(self, num_qubits: Optional[int] = None,
                 slope: float = 1,
                 offset: float = 0,
                 basis: str = 'Y',
                 name: str = 'LinRot') -> None:
        r"""Create a new linear rotation circuit.

        Args:
            num_qubits: The number of qubits representing the state :math:`|x\rangle`.
            slope: The slope of the controlled rotation.
            offset: The offset of the controlled rotation.
            basis: The type of Pauli rotation ('X', 'Y', 'Z').
            name: The name of the circuit object.
        """
        if num_qubits:
            super().__init__(num_qubits, name=name)
        else:
            super().__init__(name=name)

        # define internal parameters
        self._basis = None
        self._slope = None
        self._offset = None

        # store parameters
        self.basis = basis
        self.slope = slope
        self.offset = offset

    @property
    def basis(self) -> str:
        """The kind of Pauli rotation to be used.

        Set the basis to 'X', 'Y' or 'Z' for controlled-X, -Y, or -Z rotations respectively.

        Returns:
            The kind of Pauli rotation used in controlled rotation.
        """
        return self._basis

    @basis.setter
    def basis(self, basis: str) -> None:
        """Set the kind of Pauli rotation to be used.

        Args:
            basis: The Pauli rotation to be used.

        Raises:
            ValueError: The provided basis in not X, Y or Z.
        """
        basis = basis.lower()
        if self._basis is None or basis != self._basis:
            if basis not in ['x', 'y', 'z']:
                raise ValueError('The provided basis must be X, Y or Z, not {}'.format(basis))
            self._basis = basis
            self._data = None

    @property
    def slope(self) -> float:
        """The multiplicative factor in the rotation angle of the controlled rotations.

        The rotation angles are ``slope * 2^0``, ``slope * 2^1``, ... , ``slope * 2^(n-1)`` where
        ``n`` is the number of state qubits.

        Returns:
            The rotation angle common in all controlled rotations.
        """
        return self._slope

    @slope.setter
    def slope(self, slope: float) -> None:
        """Set the multiplicative factor of the rotation angles.

        Args:
            The slope of the rotation angles.
        """
        if self._slope is None or slope != self._slope:
            self._slope = slope
            self._data = None

    @property
    def offset(self) -> float:
        """The angle of the single qubit offset rotation on the target qubit.

        Before applying the controlled rotations, a single rotation of angle ``offset`` is
        applied to the target qubit.

        Returns:
            The offset angle.
        """
        return self._offset

    @offset.setter
    def offset(self, offset: float) -> None:
        """Set the angle for the offset rotation on the target qubit.

        Args:
            offset: The offset rotation angle.
        """
        if self._offset is None or offset != self._offset:
            self._offset = offset
            self._data = None

    @QuantumCircuit.num_qubits.setter
    def num_qubits(self, num_qubits: int) -> None:
        """Set the number of qubits.

        Note that this changes the underlying quantum register.

        Args:
            num_qubits: The new number of qubits.
        """
        if num_qubits != super().num_qubits:  # using self.num_qubits is disallowed by pylint
            self._data = None

            # set new register of appropriate size
            qr = QuantumRegister(num_qubits, name='q')
            self.qregs = [qr]

    def _configuration_is_valid(self, raise_on_failure: bool = True) -> bool:
        valid = True

        if self.num_qubits is None:
            valid = False
            if raise_on_failure:
                raise AttributeError('The number of qubits has not been set.')

        return valid

    @property
    def data(self) -> List[Tuple[Instruction, List[Qubit], List[Clbit]]]:
        """Get the circuit definition."""
        if self._data is None:
            self._build()
        return super().data
        # return QuantumCircuitData(self)

    def _build(self):
        if self._data:
            return

        self._data = []

        _ = self._configuration_is_valid()

        qr_state, qr_target = self.qubits[:-1], self.qubits[-1]

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
