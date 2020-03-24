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

"""Fixed Value Comparator."""

from typing import List, Optional
import numpy as np

from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.circuit.exceptions import CircuitError
from qiskit.aqua.circuits.gates import logical_or  # pylint: disable=unused-import


class FixedValueComparator(QuantumCircuit):
    r"""Fixed Value Comparator.

    Operator compares basis states \|i>_n against a classically
    given fixed value L and flips a target qubit if i >= L (or < depending on parameters):

        \|i>_n\|0> --> \|i>_n\|1> if i >= L else \|i>\|0>

    Operator is based on two's complement implementation of binary
    subtraction but only uses carry bits and no actual result bits.
    If the most significant carry bit (= results bit) is 1, the ">="
    condition is True otherwise it is False.
    """

    def __init__(self, *regs, value: int, geq: bool = True,
                 num_state_qubits: Optional[int] = None, name='cmp') -> None:
        """
        Args:
            regs: The qubit registers.
            value: The fixed value to compare with.
            geq: Evaluate ">=" condition of "<" condition.
            num_state_qubits: Number of state qubits. If this is set it will determine the number
                of qubits required for the circuit.
            name: Name of the circuit.

        Raises:
            CircuitError: If ``num_state_qubits`` is set and the determined number of qubits is
                not compatible with the qubits provided in the registers.
        """
        super().__init__(*regs, name=name)

        if num_state_qubits:
            required_num_qubits = 2 * num_state_qubits

            # if no qubits have been set yet, set them
            if self.qregs == []:
                self.add_register(required_num_qubits)
            # else check if compatible
            elif self.n_qubits < required_num_qubits:
                raise CircuitError(
                    'For {} state qubits a total of {} qubits are required, but \
                     only {} are in the circuit'.format(num_state_qubits, required_num_qubits,
                                                        self.n_qubits)
                )
        # infer the number of state qubits
        else:
            # store internals
        self._num_state_qubits = num_state_qubits
        self._value = value
        self._geq = geq

        # set up state and target registers
        i_state =
        qr_result = QuantumRegister(1, 'result')
        self._num_state_qubits = num_state_qubits

        super().__init__(qr_state, qr_result)

        # add ancilla register
        if self.num_ancilla_qubits > 0:
            qr_ancilla = QuantumRegister(self.num_ancilla_qubits, 'ancilla')
            self.add_register(qr_ancilla)
        else:
            qr_ancilla = None

        # build circuit
        self._build(qr_state, qr_result, qr_ancilla)

    @property
    def value(self) -> int:
        """The value to compare the qubit register to.

        Returns:
            The value against which the value of the qubit register is compared.
        """
        return self._value

    @property
    def num_state_qubits(self) -> int:
        """The number of qubits encoding the state for the comparison.

        Returns:
            The number of state qubits.
        """
        return self._num_state_qubits

    @property
    def num_ancilla_qubits(self) -> int:
        """The number of ancilla qubits used.

        Returns:
            The number of ancillas in the circuit.
        """
        return self._num_state_qubits - 1

    def _get_twos_complement(self) -> List[int]:
        """Returns the 2's complement of self.value as array.

        Returns:
             The 2's complement of self.value.
        """

        twos_complement = pow(2, self.num_state_qubits) - int(np.ceil(self.value))
        twos_complement = '{0:b}'.format(twos_complement).rjust(self.num_state_qubits, '0')
        twos_complement = \
            [1 if twos_complement[i] == '1' else 0 for i in reversed(range(len(twos_complement)))]
        return twos_complement

    def _build(self,
               qr_state: QuantumRegister,
               qr_result: QuantumRegister,
               qr_ancilla: QuantumRegister) -> None:
        """Build the comparator circuit.

        Args:
            qr_state: The register containing the qubit state.
            qr_result: The register containing the single qubit, which will contain the result.
            qr_ancilla: The register containing the ancilla qubits.
        """
        if self.value <= 0:  # condition always satisfied for non-positive values
            if self._geq:  # otherwise the condition is never satisfied
                self.x(qr_result)
        # condition never satisfied for values larger than or equal to 2^n
        elif self.value < pow(2, self.num_state_qubits):

            if self.num_state_qubits > 1:

                twos = self._get_twos_complement()
                for i in range(self.num_state_qubits):
                    if i == 0:
                        if twos[i] == 1:
                            self.cx(qr_state[i], qr_ancilla[i])
                    elif i < self.num_state_qubits-1:
                        if twos[i] == 1:
                            self.OR([qr_state[i], qr_ancilla[i-1]], qr_ancilla[i], None)
                        else:
                            self.ccx(qr_state[i], qr_ancilla[i-1], qr_ancilla[i])
                    else:
                        if twos[i] == 1:
                            # OR needs the result argument as qubit not register, thus
                            # access the index [0]
                            self.OR([qr_state[i], qr_ancilla[i-1]], qr_result[0], None)
                        else:
                            self.ccx(qr_state[i], qr_ancilla[i-1], qr_result)

                # flip result bit if geq flag is false
                if not self._geq:
                    self.x(qr_result[0])

                # uncompute ancillas state
                for i in reversed(range(self.num_state_qubits-1)):
                    if i == 0:
                        if twos[i] == 1:
                            self.cx(qr_state[i], qr_ancilla[i])
                    else:
                        if twos[i] == 1:
                            self.OR([qr_state[i], qr_ancilla[i - 1]], qr_ancilla[i], None)
                        else:
                            self.ccx(qr_state[i], qr_ancilla[i - 1], qr_ancilla[i])
            else:

                # num_state_qubits == 1 and value == 1:
                self.cx(qr_state[0], qr_result)

                # flip result bit if geq flag is false
                if not self._geq:
                    self.x(qr_result)

        else:
            if not self._geq:  # otherwise the condition is never satisfied
                self.x(qr_result)
