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

# pylint: disable=no-member


"""Multi-controlled X gate."""

from qiskit.circuit import QuantumCircuit


class MCXGate(QuantumCircuit):
    """The general, multi-controlled X gate."""

    def __new__(cls, num_ctrl_qubits=None, label=None, ctrl_state=None):
        """Create a new MCX instance.

        Depending on the number of controls, this creates an explicit X, CX, CCX, C3X or C4X
        instance or a generic MCX gate.
        """
        # these gates will always be implemented for all modes of the MCX if the number of control
        # qubits matches this
        explicit = {
            1: CXGate,
            2: CCXGate
        }
        if num_ctrl_qubits == 0:
            return XGate(label=label)
        if num_ctrl_qubits in explicit.keys():
            gate_class = explicit[num_ctrl_qubits]
            gate = gate_class.__new__(gate_class, label=label, ctrl_state=ctrl_state)
            # if __new__ does not return the same type as cls, init is not called
            gate.__init__(label=label, ctrl_state=ctrl_state)
            return gate
        return super().__new__(cls)

    def __init__(self, num_ctrl_qubits, mode='noancilla', ctrl_state=None, name='mcx'):
        """Create new MCX gate."""
        available_implementations = {
            'noancilla': MCXGrayCode(num_ctrl_qubits),
            'recursion': MCXRecursive(num_ctrl_qubits),
            'v-chain': MCXVChain(num_ctrl_qubits, False),
            'v-chain-dirty': MCXVChain(num_ctrl_qubits, dirty_ancillas=True),
            # outdated, previous names
            'advanced': MCXRecursive(num_ctrl_qubits),
            'basic': MCXVChain(num_ctrl_qubits, dirty_ancillas=False),
            'basic-dirty-ancilla': MCXVChain(num_ctrl_qubits, dirty_ancillas=True)
        }

        if mode not in available_implementations.keys():
            raise AttributeError('Mode {} not supported, choose one of: {}'.format(
                mode, list(available_implementations.keys()))
            )
        num_ancilla_qubits = self.get_num_ancilla_qubits(num_ctrl_qubits, mode)
        super().__init__(num_ctrl_qubits + 1 + num_ancilla_qubits, name=name)
        self._build()

    @staticmethod
    def get_num_ancilla_qubits(num_ctrl_qubits, mode='noancilla'):
        """Get the number of required ancilla qubits without instantiating the class.

        This staticmethod might be necessary to check the number of ancillas before
        creating the gate, or to use the number of ancillas in the initialization.
        """
        if mode == 'noancilla':
            return 0
        if mode in ['recursion', 'advanced']:
            return int(num_ctrl_qubits > 4)
        if mode[:7] == 'v-chain' or mode[:5] == 'basic':
            return max(0, num_ctrl_qubits - 2)
        raise AttributeError('Unsupported mode ({}) specified!'.format(mode))

    def _build(self):

        # check ancilla input
        if ancilla_qubits:
            _ = self.qbit_argument_conversion(ancilla_qubits)

        try:
            gate = available_implementations[mode]
        except KeyError:
            all_modes = list(available_implementations.keys())
            raise ValueError('Unsupported mode ({}) selected, choose one of {}'.format(mode,
                                                                                       all_modes))

        if hasattr(gate, 'num_ancilla_qubits') and gate.num_ancilla_qubits > 0:
            required = gate.num_ancilla_qubits
            if ancilla_qubits is None:
                raise AttributeError('No ancillas provided, but {} are needed!'.format(required))

            # convert ancilla qubits to a list if they were passed as int or qubit
            if not hasattr(ancilla_qubits, '__len__'):
                ancilla_qubits = [ancilla_qubits]

            if len(ancilla_qubits) < required:
                actually = len(ancilla_qubits)
                raise ValueError('At least {} ancillas required, but {} given.'.format(required,
                                                                                       actually))
            # size down if too many ancillas were provided
            ancilla_qubits = ancilla_qubits[:required]
        else:
            ancilla_qubits = []

        return self.append(gate, control_qubits[:] + [target_qubit] + ancilla_qubits[:], [])

    @property
    def num_ancilla_qubits(self):
        """The number of ancilla qubits."""
        return self.get_num_ancilla_qubits(self.num_ctrl_qubits, mode)

    def control(self, num_ctrl_qubits=1, label=None, ctrl_state=None):
        """Return a multi-controlled-X gate with more control lines.

        Args:
            num_ctrl_qubits (int): number of control qubits.
            label (str or None): An optional label for the gate [Default: None]
            ctrl_state (int or str or None): control state expressed as integer,
                string (e.g. '110'), or None. If None, use all 1s.

        Returns:
            ControlledGate: controlled version of this gate.
        """
        if ctrl_state is None:
            # use __class__ so this works for derived classes
            gate = self.__class__(self.num_ctrl_qubits + num_ctrl_qubits, label=label,
                                  ctrl_state=ctrl_state)
            gate.base_gate.label = self.label
            return gate
        return super().control(num_ctrl_qubits, label=label, ctrl_state=ctrl_state)


class MCXGrayCode(MCXGate):
    r"""Implement the multi-controlled X gate using the Gray code.

    This delegates the implementation to the MCU1 gate, since :math:`X = H \cdot U1(\pi) \cdot H`.
    """

    def _define(self):
        """Define the MCX gate using the Gray code."""
        from .u1 import MCU1Gate
        q = QuantumRegister(self.num_qubits, name='q')
        self.definition = [
            (HGate(), [q[-1]], []),
            (MCU1Gate(numpy.pi, num_ctrl_qubits=self.num_ctrl_qubits), q[:], []),
            (HGate(), [q[-1]], [])
        ]


class MCXRecursive(MCXGate):
    """Implement the multi-controlled X gate using recursion.

    Using a single ancilla qubit, the multi-controlled X gate is recursively split onto
    four sub-registers. This is done until we reach the 3- or 4-controlled X gate since
    for these we have a concrete implementation that do not require ancillas.
    """

    @staticmethod
    def get_num_ancilla_qubits(num_ctrl_qubits, mode='recursion'):
        """Get the number of required ancilla qubits."""
        return MCXGate.get_num_ancilla_qubits(num_ctrl_qubits, mode)

    def _define(self):
        """Define the MCX gate using recursion."""
        q = QuantumRegister(self.num_qubits, name='q')
        if self.num_qubits == 4:
            self.definition = [(C3XGate(), q[:], [])]
        elif self.num_qubits == 5:
            self.definition = [(C4XGate(), q[:], [])]
        else:
            self.definition = self._recurse(q[:-1], q_ancilla=q[-1])

    def _recurse(self, q, q_ancilla=None):
        # recursion stop
        if len(q) == 4:
            return [(C3XGate(), q[:], [])]
        if len(q) == 5:
            return [(C4XGate(), q[:], [])]
        if len(q) < 4:
            raise AttributeError('Something went wrong in the recursion, have less than 4 qubits.')

        # recurse
        num_ctrl_qubits = len(q) - 1
        middle = ceil(num_ctrl_qubits / 2)
        first_half = [*q[:middle], q_ancilla]
        second_half = [*q[middle:num_ctrl_qubits], q_ancilla, q[num_ctrl_qubits]]

        rule = []
        rule += self._recurse(first_half, q_ancilla=q[middle])
        rule += self._recurse(second_half, q_ancilla=q[middle - 1])
        rule += self._recurse(first_half, q_ancilla=q[middle])
        rule += self._recurse(second_half, q_ancilla=q[middle - 1])

        return rule


class MCXVChain(MCXGate):
    """Implement the multi-controlled X gate using a V-chain of CX gates."""

    def __new__(cls, num_ctrl_qubits=None, dirty_ancillas=False,  # pylint: disable=unused-argument
                label=None, ctrl_state=None):
        """Create a new MCX instance.

        This must be defined anew to include the additional argument ``dirty_ancillas``.
        """
        return super().__new__(cls, num_ctrl_qubits, label=label, ctrl_state=ctrl_state)

    def __init__(self, num_ctrl_qubits, dirty_ancillas=False, label=None, ctrl_state=None):
        super().__init__(num_ctrl_qubits, label=label, ctrl_state=ctrl_state)
        self._dirty_ancillas = dirty_ancillas

    @staticmethod
    def get_num_ancilla_qubits(num_ctrl_qubits, mode='v-chain'):
        """Get the number of required ancilla qubits."""
        return MCXGate.get_num_ancilla_qubits(num_ctrl_qubits, mode)

    def _define(self):
        """Define the MCX gate using a V-chain of CX gates."""
        q = QuantumRegister(self.num_qubits, name='q')
        q_controls = q[:self.num_ctrl_qubits]
        q_target = q[self.num_ctrl_qubits]
        q_ancillas = q[self.num_ctrl_qubits + 1:]

        definition = []

        if self._dirty_ancillas:
            i = self.num_ctrl_qubits - 3
            ancilla_pre_rule = [
                (U2Gate(0, numpy.pi), [q_target], []),
                (CXGate(), [q_target, q_ancillas[i]], []),
                (U1Gate(-numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_controls[-1], q_ancillas[i]], []),
                (U1Gate(numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_target, q_ancillas[i]], []),
                (U1Gate(-numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_controls[-1], q_ancillas[i]], []),
                (U1Gate(numpy.pi / 4), [q_ancillas[i]], []),
            ]
            for inst in ancilla_pre_rule:
                definition.append(inst)

            for j in reversed(range(2, self.num_ctrl_qubits - 1)):
                definition.append(
                    (RCCXGate(), [q_controls[j], q_ancillas[i - 1], q_ancillas[i]], []))
                i -= 1

        definition.append((RCCXGate(), [q_controls[0], q_controls[1], q_ancillas[0]], []))
        i = 0
        for j in range(2, self.num_ctrl_qubits - 1):
            definition.append((RCCXGate(), [q_controls[j], q_ancillas[i], q_ancillas[i + 1]], []))
            i += 1

        if self._dirty_ancillas:
            ancilla_post_rule = [
                (U1Gate(-numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_controls[-1], q_ancillas[i]], []),
                (U1Gate(numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_target, q_ancillas[i]], []),
                (U1Gate(-numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_controls[-1], q_ancillas[i]], []),
                (U1Gate(numpy.pi / 4), [q_ancillas[i]], []),
                (CXGate(), [q_target, q_ancillas[i]], []),
                (U2Gate(0, numpy.pi), [q_target], []),
            ]
            for inst in ancilla_post_rule:
                definition.append(inst)
        else:
            definition.append((CCXGate(), [q_controls[-1], q_ancillas[i], q_target], []))

        for j in reversed(range(2, self.num_ctrl_qubits - 1)):
            definition.append((RCCXGate(), [q_controls[j], q_ancillas[i - 1], q_ancillas[i]], []))
            i -= 1
        definition.append((RCCXGate(), [q_controls[0], q_controls[1], q_ancillas[i]], []))

        if self._dirty_ancillas:
            for i, j in enumerate(list(range(2, self.num_ctrl_qubits - 1))):
                definition.append(
                    (RCCXGate(), [q_controls[j], q_ancillas[i], q_ancillas[i + 1]], []))

        self.definition = definition
