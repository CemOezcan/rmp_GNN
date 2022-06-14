from abc import ABC, abstractmethod
from typing import List

from src.migration.normalizer import Normalizer
from src.util import MultiGraphWithPos, MultiGraph


class AbstractConnector(ABC):
    """
    Abstract superclass for the expansion of the input graph with remote edges.
    """

    def __init__(self, normalizer: Normalizer):
        """
        Initializes the remote message passing strategy.

        Parameters
        ----------
        normalizer :  Normalizer for remote edges
        """
        self._normalizer = normalizer
        self._initialize()

    @abstractmethod
    def _initialize(self):
        """
        Special initialization function if parameterized preprocessing is necessary.

        Returns
        -------

        """
        raise NotImplementedError

    @abstractmethod
    def run(self, graph: MultiGraph, clusters: List[List], is_training: bool) -> MultiGraphWithPos:
        """
        Adds remote edges to the input graph.

        Parameters
        ----------
        graph : Input graph
        clusters : Clustering of the graph
        is_training : Whether the input is a training instance or not

        Returns the input graph including remote edges.
        -------

        """
        raise NotImplementedError
