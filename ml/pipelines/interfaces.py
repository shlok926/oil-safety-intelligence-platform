"""
Machine Learning Pipeline Interfaces
Abstract Base Classes defining pipeline contracts for SIF precursor extraction,
triad determination, and barrier evaluation without heavy runtime dependencies.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class SIFPipelineInterface(ABC):
    """Base interface for SIF detection and classification pipelines."""

    @abstractmethod
    def process_incident(self, incident_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incident report and return pipeline results.
        
        :param incident_payload: Dictionary containing incident narrative and metadata.
        :return: Pipeline output dictionary.
        """
        pass


class TriadExtractorInterface(ABC):
    """Interface for Precursor Triad (Activity, Mechanism, Energy) extraction."""

    @abstractmethod
    def extract_triad(self, narrative: str) -> Dict[str, Any]:
        """
        Extract the Precursor Triad from narrative text.
        
        :param narrative: Raw or sanitized incident narrative.
        :return: Dictionary containing activity, mechanism, energy source, and confidence scores.
        """
        pass


class BarrierEvaluatorInterface(ABC):
    """Interface for Safety Barrier state evaluation."""

    @abstractmethod
    def evaluate_barriers(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate barrier integrity and determine barrier failures/degradations.
        
        :param incident_data: Incident and triad context.
        :return: Barrier status mapping and degradation assessments.
        """
        pass
