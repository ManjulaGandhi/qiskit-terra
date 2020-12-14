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

"""The Amplitude Estimation interface."""

from abc import abstractmethod
from typing import Union, Optional, Dict, Callable, Tuple
import numpy as np
from qiskit.providers import BaseBackend, Backend
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import AlgorithmResult

from .estimation_problem import EstimationProblem


class AmplitudeEstimator:
    """The Amplitude Estimation interface."""

    def __init__(self,
                 quantum_instance: Optional[Union[Backend, BaseBackend, QuantumInstance]] = None
                 ) -> None:
        """
        Args:
            quantum_instance: The quantum instance used to run this algorithm.
        """
        self.quantum_instance = quantum_instance

    @property
    def quantum_instance(self) -> Optional[QuantumInstance]:
        """Get the quantum instance.

        Returns:
            The quantum instance used to run this algorithm.
        """
        return self._quantum_instance

    @quantum_instance.setter
    def quantum_instance(self, quantum_instance: Union[QuantumInstance,
                                                       BaseBackend, Backend]) -> None:
        """Set quantum instance.

        Args:
            quantum_instance: The quantum instance used to run this algorithm.
        """
        if isinstance(quantum_instance, (BaseBackend, Backend)):
            quantum_instance = QuantumInstance(quantum_instance)
        self._quantum_instance = quantum_instance

    @abstractmethod
    def estimate(self, estimation_problem: EstimationProblem) -> 'AmplitudeEstimatorResult':
        """Run the amplitude estimation algorithm.

        Args:
            estimation_problem: An ``EstimationProblem`` describing
        """
        raise NotImplementedError


class AmplitudeEstimatorResult(AlgorithmResult):
    """The results object for amplitude estimation algorithms."""

    @property
    def circuit_results(self) -> Optional[Union[np.ndarray, Dict[str, int]]]:
        """Return the circuit results. Can be a statevector or counts dictionary."""
        return self.get('circuit_results')

    @circuit_results.setter
    def circuit_results(self, value: Union[np.ndarray, Dict[str, int]]) -> None:
        """Set the circuit results."""
        self.data['circuit_results'] = value

    @property
    def shots(self) -> int:
        """Return the number of shots used. Is 1 for statevector-based simulations."""
        return self.get('shots')

    @shots.setter
    def shots(self, value: int) -> None:
        """Set the number of shots used."""
        self.data['shots'] = value

    @property
    def estimation(self) -> float:
        r"""Return the estimation for the amplitude in :math:`[0, 1]`."""
        return self.get('estimation')

    @estimation.setter
    def estimation(self, value: float) -> None:
        r"""Set the estimation for the amplitude in :math:`[0, 1]`."""
        self.data['estimation'] = value

    @property
    def estimation_processed(self) -> float:
        """Return the estimation for the amplitude after the post-processing has been applied."""
        return self.get('estimation_processed')

    @estimation_processed.setter
    def estimation_processed(self, value: float) -> None:
        """Set the estimation for the amplitude after the post-processing has been applied."""
        self.data['estimation_processed'] = value

    @property
    def num_oracle_queries(self) -> int:
        """Return the number of Grover oracle queries."""
        return self.get('num_oracle_queries')

    @num_oracle_queries.setter
    def num_oracle_queries(self, value: int) -> None:
        """Set the number of Grover oracle queries."""
        self.data['num_oracle_queries'] = value

    @property
    def post_processing(self) -> Callable[[float], float]:
        """Return a handle to the post processing function."""
        return self._post_processing

    @post_processing.setter
    def post_processing(self, post_processing: Callable[[float], float]) -> None:
        """Set a handle to the post processing function."""
        self._post_processing = post_processing

    @property
    def confidence_interval(self) -> Tuple[float, float]:
        """Return the confidence interval for the amplitude (95% interval by default)."""
        return self.get('confidence_interval')

    @confidence_interval.setter
    def confidence_interval(self, confidence_interval: Tuple[float, float]) -> None:
        """Set the confidence interval for the amplitude (95% interval by default)."""
        self.data['confidence_interval'] = confidence_interval

    @property
    def confidence_interval_processed(self) -> Tuple[float, float]:
        """Return the post-processed confidence interval (95% interval by default)."""
        return self.get('confidence_interval_processed')

    @confidence_interval_processed.setter
    def confidence_interval_processed(self, confidence_interval: Tuple[float, float]) -> None:
        """Set the post-processed confidence interval (95% interval by default)."""
        self.data['confidence_interval_processed'] = confidence_interval

    @staticmethod
    def from_dict(a_dict: Dict) -> 'AmplitudeEstimationAlgorithmResult':
        """Create a new result object from a dictionary."""
        return AmplitudeEstimatorResult(a_dict)
