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

# pylint: disable=invalid-name,missing-docstring

from copy import copy
from warnings import warn


class IQXStyle:
    """IBM IQX Design Style colors."""

    def __init__(self):
        # Set colors
        classic = '#9F1853'
        phase = '#D9AD3E'
        nonunitary = '#A8A8A8'
        hadamard = '#002D9C'
        # quantum = '#9F1853'
        quantum = '#33B1FF'
        other = '#33B1FF'

        self.textcol = {
            classic: '#ffffff',
            phase: '#000000',
            nonunitary: '#000000',
            hadamard: '#ffffff',
            quantum: '#000000',
            other: '#000000',
        }

        self.name = 'quantumness'
        self.tc = '#000000'
        self.sc = '#000000'
        self.lc = '#000000'
        self.not_gate_lc = '#ffffff'
        self.cc = '#778899'
        self.gc = '#ffffff'
        self.gt = '#ffffff'
        self.bc = '#bdbdbd'
        self.bg = '#ffffff'
        self.edge_color = None
        self.math_fs = 15
        self.fs = 13
        self.sfs = 8
        self.colored_add_width = 0.2
        self.disptex = {
            'id': r'\mathrm{I}',
            'u0': r'\mathrm{U}_0',
            'u1': r'\mathrm{P}',
            'u2': r'\mathrm{U}_2',
            'u3': r'\mathrm{U}_3',
            'x': r'\mathrm{X}',
            'y': r'\mathrm{Y}',
            'z': r'\mathrm{Z}',
            'h': r'\mathrm{H}',
            's': r'\mathrm{S}',
            'iswap': r'\mathrm{iSwap}',
            'dcx': r'\mathrm{DCX}',
            'ms': r'\mathrm{GMS}',
            'rccx': r'\mathrm{RCCX}',
            'rcccx': r'\mathrm{RCCCX}',
            'sdg': r'\mathrm{S}^\dagger',
            't': r'\mathrm{T}',
            'tdg': r'\mathrm{T}^\dagger',
            'r': r'\mathrm{R}',
            'rx': r'\mathrm{R}_\mathrm{X}',
            'ry': r'\mathrm{R}_\mathrm{Y}',
            'rz': r'\mathrm{R}_\mathrm{Z}',
            'rxx': r'\mathrm{R}_\mathrm{XX}',
            'ryy': r'\mathrm{R}_\mathrm{YY}',
            'rzx': r'\mathrm{R}_\mathrm{ZX}',
            'rzz': r'\mathrm{R}_\mathrm{ZZ}',
            'reset': r'\left|0\right\rangle',
        }
        self.dispcol = {
            'u0': quantum,
            'u1': phase,
            'u2': other,
            'u3': quantum,
            'id': classic,
            'x': classic,
            'y': other,
            'z': phase,
            'h': hadamard,
            'cx': classic,
            'cy': other,
            'cz': other,
            'swap': classic,
            's': phase,
            'sdg': phase,
            'dcx': classic,
            'iswap': other,
            't': phase,
            'tdg': phase,
            'r': quantum,
            'rx': quantum,
            'ry': quantum,
            'rz': quantum,
            'reset': nonunitary,
            'target': '#ffffff',
            'multi': other,
            'meas': nonunitary
        }
        self.latexmode = False
        self.bundle = True
        self.index = False
        self.figwidth = -1
        self.dpi = 150
        self.margin = [2.0, 0.1, 0.1, 0.3]
        self.cline = 'doublet'

    def set_style(self, style_dic):
        dic = copy(style_dic)
        self.tc = dic.pop('textcolor', self.tc)
        self.sc = dic.pop('subtextcolor', self.sc)
        self.lc = dic.pop('linecolor', self.lc)
        self.cc = dic.pop('creglinecolor', self.cc)
        self.gt = dic.pop('gatetextcolor', self.tc)
        self.gc = dic.pop('gatefacecolor', self.gc)
        self.bc = dic.pop('barrierfacecolor', self.bc)
        self.bg = dic.pop('backgroundcolor', self.bg)
        self.fs = dic.pop('fontsize', self.fs)
        self.sfs = dic.pop('subfontsize', self.sfs)
        self.disptex = dic.pop('displaytext', self.disptex)
        self.dispcol = dic.pop('displaycolor', self.dispcol)
        self.latexmode = dic.pop('latexdrawerstyle', self.latexmode)
        self.bundle = dic.pop('cregbundle', self.bundle)
        self.index = dic.pop('showindex', self.index)
        self.figwidth = dic.pop('figwidth', self.figwidth)
        self.dpi = dic.pop('dpi', self.dpi)
        self.margin = dic.pop('margin', self.margin)
        self.cline = dic.pop('creglinestyle', self.cline)

        if dic:
            warn('style option/s ({}) is/are not supported'.format(', '.join(dic.keys())),
                 DeprecationWarning, 2)


class PurpleIThink:
    """IBM IQX Design Style colors."""

    def __init__(self):
        # Set colors
        classic = '#002D9C'
        phase = '#33B1FF'
        nonunitary = '#A8A8A8'
        hadamard = '#FA4D56'
        # quantum = '#9F1853'
        quantum = '#8A3FFC'
        other = '#8A3FFC'

        self.textcol = {
            classic: '#ffffff',
            phase: '#000000',
            nonunitary: '#000000',
            hadamard: '#000000',
            quantum: '#ffffff',
            other: '#ffffff',
        }

        self.name = 'quantumness'
        self.tc = '#000000'
        self.sc = '#000000'
        self.lc = '#000000'
        self.not_gate_lc = '#ffffff'
        self.cc = '#778899'
        self.gc = '#ffffff'
        self.gt = '#ffffff'
        self.bc = '#bdbdbd'
        self.bg = '#ffffff'
        self.edge_color = None
        self.math_fs = 15
        self.fs = 13
        self.sfs = 8
        self.colored_add_width = 0.2
        self.disptex = {
            'id': r'\mathrm{I}',
            'u0': r'\mathrm{U}_0',
            'u1': r'\mathrm{P}',
            'u2': r'\mathrm{U}_2',
            'u3': r'\mathrm{U}_3',
            'x': r'\mathrm{X}',
            'y': r'\mathrm{Y}',
            'z': r'\mathrm{Z}',
            'h': r'\mathrm{H}',
            's': r'\mathrm{S}',
            'iswap': r'\mathrm{iSwap}',
            'dcx': r'\mathrm{DCX}',
            'ms': r'\mathrm{GMS}',
            'rccx': r'\mathrm{RCCX}',
            'rcccx': r'\mathrm{RCCCX}',
            'sdg': r'\mathrm{S}^\dagger',
            't': r'\mathrm{T}',
            'tdg': r'\mathrm{T}^\dagger',
            'r': r'\mathrm{R}',
            'rx': r'\mathrm{R}_\mathrm{X}',
            'ry': r'\mathrm{R}_\mathrm{Y}',
            'rz': r'\mathrm{R}_\mathrm{Z}',
            'rxx': r'\mathrm{R}_\mathrm{XX}',
            'ryy': r'\mathrm{R}_\mathrm{YY}',
            'rzx': r'\mathrm{R}_\mathrm{ZX}',
            'rzz': r'\mathrm{R}_\mathrm{ZZ}',
            'reset': r'\left|0\right\rangle',
        }
        self.dispcol = {
            'u0': quantum,
            'u1': phase,
            'u2': other,
            'u3': quantum,
            'id': classic,
            'x': classic,
            'y': other,
            'z': phase,
            'h': hadamard,
            'cx': classic,
            'cy': other,
            'cz': other,
            'swap': classic,
            's': phase,
            'sdg': phase,
            'dcx': classic,
            'iswap': other,
            't': phase,
            'tdg': phase,
            'r': quantum,
            'rx': quantum,
            'ry': quantum,
            'rz': quantum,
            'reset': nonunitary,
            'target': '#ffffff',
            'multi': other,
            'meas': nonunitary
        }
        self.latexmode = False
        self.bundle = True
        self.index = False
        self.figwidth = -1
        self.dpi = 150
        self.margin = [2.0, 0.1, 0.1, 0.3]
        self.cline = 'doublet'

    def set_style(self, style_dic):
        dic = copy(style_dic)
        self.tc = dic.pop('textcolor', self.tc)
        self.sc = dic.pop('subtextcolor', self.sc)
        self.lc = dic.pop('linecolor', self.lc)
        self.cc = dic.pop('creglinecolor', self.cc)
        self.gt = dic.pop('gatetextcolor', self.tc)
        self.gc = dic.pop('gatefacecolor', self.gc)
        self.bc = dic.pop('barrierfacecolor', self.bc)
        self.bg = dic.pop('backgroundcolor', self.bg)
        self.fs = dic.pop('fontsize', self.fs)
        self.sfs = dic.pop('subfontsize', self.sfs)
        self.disptex = dic.pop('displaytext', self.disptex)
        self.dispcol = dic.pop('displaycolor', self.dispcol)
        self.latexmode = dic.pop('latexdrawerstyle', self.latexmode)
        self.bundle = dic.pop('cregbundle', self.bundle)
        self.index = dic.pop('showindex', self.index)
        self.figwidth = dic.pop('figwidth', self.figwidth)
        self.dpi = dic.pop('dpi', self.dpi)
        self.margin = dic.pop('margin', self.margin)
        self.cline = dic.pop('creglinestyle', self.cline)

        if dic:
            warn('style option/s ({}) is/are not supported'.format(', '.join(dic.keys())),
                 DeprecationWarning, 2)


class _IQXStyle:
    """IBM IQX Design Style colors."""

    def __init__(self):
        # Set colors
        classic = '#002D9C'
        phase = '#33B1FF'
        nonunitary = '#A8A8A8'
        hadamard = '#FA4D56'
        quantum = '#9F1853'

        self.textcol = {
            classic: '#ffffff',
            phase: '#000000',
            nonunitary: '#000000',
            hadamard: '#000000',
            quantum: '#ffffff',
        }

        self.name = 'quantumness'
        self.tc = '#000000'
        self.sc = '#000000'
        self.lc = '#000000'
        self.not_gate_lc = '#ffffff'
        self.cc = '#778899'
        self.gc = '#ffffff'
        self.gt = '#ffffff'
        self.bc = '#bdbdbd'
        self.bg = '#ffffff'
        self.edge_color = None
        self.math_fs = 15
        self.fs = 13
        self.sfs = 8
        self.colored_add_width = 0.2
        self.disptex = {
            'id': r'\mathrm{I}',
            'u0': r'\mathrm{U}_0',
            'u1': r'\mathrm{P}',
            'u2': r'\mathrm{U}_2',
            'u3': r'\mathrm{U}_3',
            'x': r'\mathrm{X}',
            'y': r'\mathrm{Y}',
            'z': r'\mathrm{Z}',
            'h': r'\mathrm{H}',
            's': r'\mathrm{S}',
            'iswap': r'\mathrm{iSwap}',
            'dcx': r'\mathrm{DCX}',
            'ms': r'\mathrm{GMS}',
            'rccx': r'\mathrm{RCCX}',
            'rcccx': r'\mathrm{RCCCX}',
            'sdg': r'\mathrm{S}^\dagger',
            't': r'\mathrm{T}',
            'tdg': r'\mathrm{T}^\dagger',
            'r': r'\mathrm{R}',
            'rx': r'\mathrm{R}_\mathrm{X}',
            'ry': r'\mathrm{R}_\mathrm{Y}',
            'rz': r'\mathrm{R}_\mathrm{Z}',
            'rxx': r'\mathrm{R}_\mathrm{XX}',
            'ryy': r'\mathrm{R}_\mathrm{YY}',
            'rzx': r'\mathrm{R}_\mathrm{ZX}',
            'rzz': r'\mathrm{R}_\mathrm{ZZ}',
            'reset': r'\left|0\right\rangle',
        }
        self.dispcol = {
            'u0': quantum,
            'u1': phase,
            'u2': quantum,
            'u3': quantum,
            'id': classic,
            'x': classic,
            'y': quantum,
            'z': phase,
            'h': hadamard,
            'cx': classic,
            'cy': quantum,
            'cz': quantum,
            'swap': classic,
            's': phase,
            'sdg': phase,
            'dcx': classic,
            'iswap': quantum,
            't': phase,
            'tdg': phase,
            'r': quantum,
            'rx': quantum,
            'ry': quantum,
            'rz': quantum,
            'mcx': classic,
            'reset': nonunitary,
            'target': '#ffffff',
            'multi': quantum,
            'meas': nonunitary
        }
        self.latexmode = False
        self.bundle = True
        self.index = False
        self.figwidth = -1
        self.dpi = 150
        self.margin = [2.0, 0.1, 0.1, 0.3]
        self.cline = 'doublet'

    def set_style(self, style_dic):
        dic = copy(style_dic)
        self.tc = dic.pop('textcolor', self.tc)
        self.sc = dic.pop('subtextcolor', self.sc)
        self.lc = dic.pop('linecolor', self.lc)
        self.cc = dic.pop('creglinecolor', self.cc)
        self.gt = dic.pop('gatetextcolor', self.tc)
        self.gc = dic.pop('gatefacecolor', self.gc)
        self.bc = dic.pop('barrierfacecolor', self.bc)
        self.bg = dic.pop('backgroundcolor', self.bg)
        self.fs = dic.pop('fontsize', self.fs)
        self.sfs = dic.pop('subfontsize', self.sfs)
        self.disptex = dic.pop('displaytext', self.disptex)
        self.dispcol = dic.pop('displaycolor', self.dispcol)
        self.latexmode = dic.pop('latexdrawerstyle', self.latexmode)
        self.bundle = dic.pop('cregbundle', self.bundle)
        self.index = dic.pop('showindex', self.index)
        self.figwidth = dic.pop('figwidth', self.figwidth)
        self.dpi = dic.pop('dpi', self.dpi)
        self.margin = dic.pop('margin', self.margin)
        self.cline = dic.pop('creglinestyle', self.cline)

        if dic:
            warn('style option/s ({}) is/are not supported'.format(', '.join(dic.keys())),
                 DeprecationWarning, 2)


class OldStyle:
    """IBM IQX Design Style colors."""

    def __init__(self):
        # Set colors
        basis_color = '#D2A106'
        clifford_color = '#33B1FF'
        non_gate_color = '#000000'
        other_color = '#002D9C'
        pauli_color = '#9F1853'
        iden_color = '#9F1853'
        self.textcol = {
            basis_color: '#000000',
            clifford_color: '#000000',
            non_gate_color: '#ffffff',
            other_color: '#ffffff',
            pauli_color: '#ffffff',
            iden_color: '#ffffff',
        }

        self.name = 'iqx'
        self.tc = '#000000'
        self.sc = '#000000'
        self.lc = '#000000'
        self.not_gate_lc = '#ffffff'
        self.cc = '#778899'
        self.gc = '#ffffff'
        self.gt = '#ffffff'
        self.bc = '#bdbdbd'
        self.bg = '#ffffff'
        self.edge_color = None
        self.math_fs = 15
        self.fs = 13
        self.sfs = 8
        self.colored_add_width = 0.2
        self.disptex = {
            'id': r'\mathrm{I}',
            'u0': r'\mathrm{U}_0',
            'u1': r'\mathrm{P}',
            'u2': r'\mathrm{U}_2',
            'u3': r'\mathrm{U}_3',
            'x': r'\mathrm{X}',
            'y': r'\mathrm{Y}',
            'z': r'\mathrm{Z}',
            'h': r'\mathrm{H}',
            's': r'\mathrm{S}',
            'iswap': r'\mathrm{iSwap}',
            'dcx': r'\mathrm{DCX}',
            'ms': r'\mathrm{GMS}',
            'rccx': r'\mathrm{RCCX}',
            'rcccx': r'\mathrm{RCCCX}',
            'sdg': r'\mathrm{S}^\dagger',
            't': r'\mathrm{T}',
            'tdg': r'\mathrm{T}^\dagger',
            'r': r'\mathrm{R}',
            'rx': r'\mathrm{R}_\mathrm{X}',
            'ry': r'\mathrm{R}_\mathrm{Y}',
            'rz': r'\mathrm{R}_\mathrm{Z}',
            'rxx': r'\mathrm{R}_\mathrm{XX}',
            'ryy': r'\mathrm{R}_\mathrm{YY}',
            'rzx': r'\mathrm{R}_\mathrm{ZX}',
            'rzz': r'\mathrm{R}_\mathrm{ZZ}',
            'reset': r'\left|0\right\rangle',
        }
        self.dispcol = {
            'u0': basis_color,
            'u1': basis_color,
            'u2': basis_color,
            'u3': basis_color,
            'id': iden_color,
            'x': pauli_color,
            'y': pauli_color,
            'z': pauli_color,
            'h': clifford_color,
            'cx': clifford_color,
            'cy': clifford_color,
            'cz': clifford_color,
            'swap': clifford_color,
            's': clifford_color,
            'sdg': clifford_color,
            'dcx': clifford_color,
            'iswap': clifford_color,
            't': other_color,
            'tdg': other_color,
            'r': other_color,
            'rx': other_color,
            'ry': other_color,
            'rz': other_color,
            'reset': non_gate_color,
            'target': '#ffffff',
            'multi': other_color,
            'meas': non_gate_color
        }
        self.latexmode = False
        self.bundle = True
        self.index = False
        self.figwidth = -1
        self.dpi = 150
        self.margin = [2.0, 0.1, 0.1, 0.3]
        self.cline = 'doublet'

    def set_style(self, style_dic):
        dic = copy(style_dic)
        self.tc = dic.pop('textcolor', self.tc)
        self.sc = dic.pop('subtextcolor', self.sc)
        self.lc = dic.pop('linecolor', self.lc)
        self.cc = dic.pop('creglinecolor', self.cc)
        self.gt = dic.pop('gatetextcolor', self.tc)
        self.gc = dic.pop('gatefacecolor', self.gc)
        self.bc = dic.pop('barrierfacecolor', self.bc)
        self.bg = dic.pop('backgroundcolor', self.bg)
        self.fs = dic.pop('fontsize', self.fs)
        self.sfs = dic.pop('subfontsize', self.sfs)
        self.disptex = dic.pop('displaytext', self.disptex)
        self.dispcol = dic.pop('displaycolor', self.dispcol)
        self.latexmode = dic.pop('latexdrawerstyle', self.latexmode)
        self.bundle = dic.pop('cregbundle', self.bundle)
        self.index = dic.pop('showindex', self.index)
        self.figwidth = dic.pop('figwidth', self.figwidth)
        self.dpi = dic.pop('dpi', self.dpi)
        self.margin = dic.pop('margin', self.margin)
        self.cline = dic.pop('creglinestyle', self.cline)

        if dic:
            warn('style option/s ({}) is/are not supported'.format(', '.join(dic.keys())),
                 DeprecationWarning, 2)


class DefaultStyle:
    """IBM Design Style colors
    """

    def __init__(self):
        # Set colors
        basis_color = '#FA74A6'
        clifford_color = '#6FA4FF'
        non_gate_color = '#000000'
        other_color = '#BB8BFF'
        pauli_color = '#05BAB6'
        iden_color = '#05BAB6'

        self.name = 'legacy'
        self.tc = '#000000'
        self.sc = '#000000'
        self.lc = '#000000'
        self.not_gate_lc = '#ffffff'
        self.cc = '#778899'
        self.gc = '#ffffff'
        self.gt = '#000000'
        self.bc = '#bdbdbd'
        self.bg = '#ffffff'
        self.edge_color = None
        self.math_fs = 15
        self.fs = 13
        self.sfs = 8
        self.colored_add_width = 0.2
        self.disptex = {
            'id': 'I',
            'u0': 'U_0',
            'u1': 'U_1',
            'u2': 'U_2',
            'u3': 'U_3',
            'x': 'X',
            'y': 'Y',
            'z': 'Z',
            'h': 'H',
            's': 'S',
            'sdg': 'S^\\dagger',
            't': 'T',
            'tdg': 'T^\\dagger',
            'r': 'R',
            'rx': 'R_x',
            'ry': 'R_y',
            'rz': 'R_z',
            'reset': '\\left|0\\right\\rangle'
        }
        self.dispcol = {
            'u0': basis_color,
            'u1': basis_color,
            'u2': basis_color,
            'u3': basis_color,
            'id': iden_color,
            'x': pauli_color,
            'y': pauli_color,
            'z': pauli_color,
            'h': clifford_color,
            'cx': clifford_color,
            'cy': clifford_color,
            'cz': clifford_color,
            'swap': clifford_color,
            's': clifford_color,
            'sdg': clifford_color,
            'dcx': clifford_color,
            'iswap': clifford_color,
            't': other_color,
            'tdg': other_color,
            'r': other_color,
            'rx': other_color,
            'ry': other_color,
            'rz': other_color,
            'reset': non_gate_color,
            'target': '#ffffff',
            'multi': other_color,
            'meas': non_gate_color
        }
        self.latexmode = False
        self.bundle = True
        self.index = False
        self.figwidth = -1
        self.dpi = 150
        self.margin = [2.0, 0.1, 0.1, 0.3]
        self.cline = 'doublet'

    def set_style(self, style_dic):
        dic = copy(style_dic)
        self.tc = dic.pop('textcolor', self.tc)
        self.sc = dic.pop('subtextcolor', self.sc)
        self.lc = dic.pop('linecolor', self.lc)
        self.cc = dic.pop('creglinecolor', self.cc)
        self.gt = dic.pop('gatetextcolor', self.tc)
        self.gc = dic.pop('gatefacecolor', self.gc)
        self.bc = dic.pop('barrierfacecolor', self.bc)
        self.bg = dic.pop('backgroundcolor', self.bg)
        self.fs = dic.pop('fontsize', self.fs)
        self.sfs = dic.pop('subfontsize', self.sfs)
        self.disptex = dic.pop('displaytext', self.disptex)
        self.dispcol = dic.pop('displaycolor', self.dispcol)
        self.latexmode = dic.pop('latexdrawerstyle', self.latexmode)
        self.bundle = dic.pop('cregbundle', self.bundle)
        self.index = dic.pop('showindex', self.index)
        self.figwidth = dic.pop('figwidth', self.figwidth)
        self.dpi = dic.pop('dpi', self.dpi)
        self.margin = dic.pop('margin', self.margin)
        self.cline = dic.pop('creglinestyle', self.cline)

        if dic:
            warn('style option/s ({}) is/are not supported'.format(', '.join(dic.keys())),
                 DeprecationWarning, 2)


class BWStyle:
    def __init__(self):
        self.name = 'bw'
        self.tc = '#000000'
        self.sc = '#000000'
        self.lc = '#000000'
        self.not_gate_lc = '#000000'
        self.cc = '#778899'
        self.gc = '#ffffff'
        self.gt = '#000000'
        self.bc = '#bdbdbd'
        self.bg = '#ffffff'
        self.edge_color = '#000000'
        self.fs = 13
        self.math_fs = 15
        self.colored_add_width = 0.2
        self.sfs = 8
        self.disptex = {
            'id': 'I',
            'u0': 'U_0',
            'u1': 'U_1',
            'u2': 'U_2',
            'u3': 'U_3',
            'x': 'X',
            'y': 'Y',
            'z': 'Z',
            'h': 'H',
            's': 'S',
            'sdg': 'S^\\dagger',
            't': 'T',
            'tdg': 'T^\\dagger',
            'r': 'R',
            'rx': 'R_x',
            'ry': 'R_y',
            'rz': 'R_z',
            'reset': '\\left|0\\right\\rangle'
        }
        self.dispcol = {
            'id': '#ffffff',
            'u0': '#ffffff',
            'u1': '#ffffff',
            'u2': '#ffffff',
            'u3': '#ffffff',
            'x': '#ffffff',
            'y': '#ffffff',
            'z': '#ffffff',
            'h': '#ffffff',
            'cx': '#000000',
            's': '#ffffff',
            'sdg': '#ffffff',
            't': '#ffffff',
            'tdg': '#ffffff',
            'r': '#ffffff',
            'rx': '#ffffff',
            'ry': '#ffffff',
            'rz': '#ffffff',
            'reset': '#ffffff',
            'target': '#ffffff',
            'meas': '#ffffff',
            'swap': '#000000',
            'multi': '#000000'
        }
        self.latexmode = False
        self.bundle = True
        self.index = False
        self.figwidth = -1
        self.dpi = 150
        self.margin = [2.0, 0.0, 0.0, 0.3]
        self.cline = 'doublet'

    def set_style(self, style_dic):
        dic = copy(style_dic)
        self.tc = dic.pop('textcolor', self.tc)
        self.sc = dic.pop('subtextcolor', self.sc)
        self.lc = dic.pop('linecolor', self.lc)
        self.cc = dic.pop('creglinecolor', self.cc)
        self.gt = dic.pop('gatetextcolor', self.tc)
        self.gc = dic.pop('gatefacecolor', self.gc)
        self.bc = dic.pop('barrierfacecolor', self.bc)
        self.bg = dic.pop('backgroundcolor', self.bg)
        self.fs = dic.pop('fontsize', self.fs)
        self.sfs = dic.pop('subfontsize', self.sfs)
        self.disptex = dic.pop('displaytext', self.disptex)
        for key in self.dispcol.keys():
            self.dispcol[key] = self.gc
        self.dispcol = dic.pop('displaycolor', self.dispcol)
        self.latexmode = dic.pop('latexdrawerstyle', self.latexmode)
        self.bundle = dic.pop('cregbundle', self.bundle)
        self.index = dic.pop('showindex', self.index)
        self.figwidth = dic.pop('figwidth', self.figwidth)
        self.dpi = dic.pop('dpi', self.dpi)
        self.margin = dic.pop('margin', self.margin)
        self.cline = dic.pop('creglinestyle', self.cline)

        if dic:
            warn('style option/s ({}) is/are not supported'.format(', '.join(dic.keys())),
                 DeprecationWarning, 2)
