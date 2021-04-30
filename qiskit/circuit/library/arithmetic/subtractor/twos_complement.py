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

"""Compute Two's Complement of a given qubit."""

from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
from qiskit.circuit.library.arithmetic import QFTAdder

class TwosComplement(QuantumCircuit):
    r"""A circuit that obtains Two's Complement on one qubit register.
    Circuit to compute the two's complement of one qubit register Part from [1].
    
    As an example, a Two's Complement circuit that performs two's complement on a 3-qubit sized
    register is as follows:

    .. parsed-literal::
    
                    ░ ┌───┐ ░                      ░
            cin_0: ─░─┤ X ├─░────────■────■────────░─
                    ░ └───┘ ░ ┌───┐  │  ┌─┴─┐      ░
        input_b_0: ─░───────░─┤ X ├──■──┤ X ├──────░─
                    ░       ░ ├───┤  │  └───┘      ░
        input_b_1: ─░───────░─┤ X ├──┼────■────■───░─
                    ░       ░ ├───┤  │    │    │   ░
        input_b_2: ─░───────░─┤ X ├──┼────┼────┼───░─
                    ░       ░ └───┘┌─┴─┐  │  ┌─┴─┐ ░
           cout_0: ─░───────░──────┤ X ├──■──┤ X ├─░─
                    ░       ░      └───┘┌─┴─┐└───┘ ░
           cout_1: ─░───────░───────────┤ X ├──────░─
                    ░       ░           └───┘      ░
           cout_2: ─░───────░──────────────────────░─
                    ░       ░                      ░


   
    **Reference**

    [1] Rahul Pratap Singh et al.,Quantum algorithm for sum of infinite series;
    determining the value of pi, `<https://www.researchgate.net/publication/329629442>`_ 

    """

    def __init__(self, 
                 num_state_qubits: int, 
                 adder: str = 'QFTAdder',
                 name: str = 'TwosComplement'
                 ) -> None:
        """
        Args:
            num_state_qubits: The size of the register.
            name: The name of the circuit.
        Raises:
            ValueError: If ``num_state_qubits`` is lower than 1.
        """
        
        if num_state_qubits < 1:
            raise ValueError('The number of qubits must be at least 1.')
        if adder is None:
            adder = QFTAdder(num_state_qubits)
        # get the number of qubits needed
        num_qubits = adder.num_qubits
        num_helper_qubits = adder.num_ancillas
        num_carry_qubits = num_qubits - 2 * num_state_qubits - num_helper_qubits
        # construct the registers
        #qr_a = QuantumRegister(num_state_qubits, 'a')  # input a
        #qr_b = QuantumRegister(num_state_qubits, 'b')  # input b
        # initialize the circuit
        #super().__init__(qr_a, qr_b)
        # add carry qubits if required
        # define the registers
        b_qr = QuantumRegister(num_state_qubits, name='input_b')
        one_qr = AncillaRegister(num_state_qubits, name='cin')
        #qr_cin = QuantumRegister(1, name='cin')
        #qr_cout = QuantumRegister(num_state_qubits, name='cout')

        # initialize the circuit
        super().__init__(b_qr, one_qr, name=name)
        #if num_carry_qubits > 0:
        #    qr_c = QuantumRegister(num_carry_qubits)
        #    self.add_register(qr_c)
        # adder helper qubits if required
        #if num_helper_qubits > 0:
        #    qr_h = AncillaRegister(num_helper_qubits)  # helper/ancilla qubits
        #    self.add_register(qr_h)
        
        # Build a temporary subcircuit that obtains two's complement of b,


    #flippling circuit and adding 1
        self.barrier()
        self.x(one_qr[0])
        self.barrier()
        for j in range(num_state_qubits):
            self.x(b_qr[j])
        self.append(QFTAdder(num_state_qubits,modular=True),one_qr[:]+b_qr[:])
        self.x(one_qr[0])
        #self.ccx(qr_cin,qr_b[0],qr_cout[0])
        #self.cx(qr_cin,qr_b[0])

        #for j in range(num_state_qubits-2):
        #    self.ccx(qr_b[j+1],qr_cout[j],qr_cout[j+1])
        #    self.cx(qr_b[j+1],qr_cout[j])
        #self.barrier()
        #flipping the left most bit
 #       self.cx(qr_cout[2],qr_cout[3])
 #       self.cx(qr_cout[3],qr_cout[2])
        #qr_z = QuantumRegister(1, name='carry_out')
        #qr_c = AncillaRegister(1, name='carry_in')
        
