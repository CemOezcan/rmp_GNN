from abc import ABC, abstractmethod


class AbstractClusteringAlgorithm(ABC):

    def __init__(self):
        self._num_clusters = 0
        self._initialize()

    @abstractmethod
    def _initialize(self):
        raise NotImplementedError

    @abstractmethod
    def run(self, graph):
        raise NotImplementedError
