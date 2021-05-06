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

"""Compute the difference of two qubit registers using Two's Complement Subtraction."""
from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
#from qiskit.circuit.library.arithmetic.adders.adder import Adder
from qiskit.circuit.library.arithmetic.adders import RippleCarryAdder,QFTAdder,ClassicalAdder
from qiskit.circuit.library.arithmetic.subtractor import TwosComplement
class Subtractor(QuantumCircuit):
    r"""A circuit that uses Two's Complement Subtraction to perform in-place subtraction on two qubit registers.

     Circuit to compute the difference of two qubit registers.
     Given two equally sized input registers that store quantum states
    :math:`|a\rangle` and :math:`|b\rangle`, performs subtraction of numbers that
    can be represented by the states, storing the resulting state in-place in the second register:

    .. math::

        |a\rangle |b\rangle \mapsto |a\rangle |a-b\rangle

    Here :math:`|a\rangle` (and correspondingly :math:`|b\rangle`) stands for the direct product
    :math:`|a_n\rangle \otimes |a_{n-1}\rangle \ldots |a_{1}\rangle \otimes |a_{0}\rangle`
    which denotes a quantum register prepared with the value :math:`a = 2^{0}a_{0} + 2^{1}a_{1} +
    \ldots 2^{n}a_{n}`[1].
    As an example, a subtractor circuit that performs two's complement on :math:`|b\rangle`and 
    performs addition on two 3-qubit sized registers is as follows:

    .. parsed-literal::

                                 ┌──────┐┌──────┐                     ┌──────┐┌──────┐
         a_0: ───────────────────┤0     ├┤2     ├─────────────────────┤2     ├┤0     ├
                                 │      ││      │┌──────┐     ┌──────┐│      ││      │
         a_1: ───────────────────┤      ├┤0     ├┤2     ├─────┤2     ├┤0     ├┤      ├
                                 │      ││      ││      │     │      ││      ││      │
         a_2: ───────────────────┤      ├┤  MAJ ├┤0     ├──■──┤0     ├┤  UMA ├┤      ├
              ┌─────────────────┐│      ││      ││      │  │  │      ││      ││      │
         b_0: ┤0                ├┤1     ├┤      ├┤  MAJ ├──┼──┤  UMA ├┤      ├┤1     ├
              │                 ││  MAJ ││      ││      │  │  │      ││      ││  UMA │
         b_1: ┤1 Twoscomplement ├┤      ├┤1     ├┤      ├──┼──┤      ├┤1     ├┤      ├
              │                 ││      │└──────┘│      │  │  │      │└──────┘│      │
         b_2: ┤2                ├┤      ├────────┤1     ├──┼──┤1     ├────────┤      ├
              └─────────────────┘│      │        └──────┘┌─┴─┐└──────┘        │      │
        q0_0: ───────────────────┤      ├────────────────┤ X ├────────────────┤      ├
                                 │      │                └───┘                │      │
        a0_0: ───────────────────┤2     ├─────────────────────────────────────┤2     ├
                                 └──────┘                                     └──────┘
    **References**
    
    [1] Vedral et al., Quantum Networks for Elementary Arithmetic Operations, 1995.
    `arXiv:quant-ph/9511018 <https://arxiv.org/pdf/quant-ph/9511018.pdf>`_
    """

    #def __init__(self, num_state_qubits: int, adder: Optional[adder] = None):
    def __init__(self, num_state_qubits: int, adder=None):
        if adder is None:
            adder = RippleCarryAdder(num_state_qubits)
        twos_complement = TwosComplement(num_state_qubits)
        # get the number of qubits needed
        num_qubits = adder.num_qubits
        num_helper_qubits = max(adder.num_ancillas,twos_complement.num_ancillas)
        num_carry_qubits = num_qubits - 2 * num_state_qubits - num_helper_qubits
        # construct the registers
        qr_a = QuantumRegister(num_state_qubits, 'a')  # input a
        qr_b = QuantumRegister(num_state_qubits, 'b')  # input b
        # initialize the circuit
        super().__init__(qr_a, qr_b)
        # add carry qubits if required
        if num_carry_qubits > 0:
            qr_c = QuantumRegister(num_carry_qubits)
            self.add_register(qr_c)
        # adder helper qubits if required
        if num_helper_qubits > 0:
            qr_h=AncillaRegister(num_helper_qubits)
            self.add_register(qr_h)
        
        self.compose(twos_complement, qubits=qr_b[:]+qr_h[:twos_complement.num_ancillas],inplace=True)
        # adder
        self.compose(adder, inplace=True)



