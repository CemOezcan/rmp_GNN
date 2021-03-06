from src.migration.normalizer import Normalizer
from src.rmp.hierarchical_connector import HierarchicalConnector
from src.rmp.random_clustering import RandomClustering
from src.rmp.hdbscan import HDBSCAN
from src.rmp.multigraph_connector import MultigraphConnector
from src.util import MultiGraphWithPos, device, EdgeSet, MultiGraph


class RemoteMessagePassing:
    """
    Remote message passing for graph neural networks.
    """
    def __init__(self, intra, inter):
        """
        Initialize the remote message passing strategy.
        """
        # TODO: Parameterize
        self._clustering_algorithm = HDBSCAN()
        self._node_connector = HierarchicalConnector(intra, inter)
        self._clusters = None

    def create_graph(self, graph: MultiGraphWithPos, is_training: bool) -> MultiGraph:
        """
        Template method: Identify clusters and connect them using remote edges.

        Parameters
        ----------
        graph : Input graph
        is_training : Whether the input is a training instance or not

        Returns the input graph with additional edges for remote message passing.
        -------

        """
        # TODO: Replace lists with tensors
        graph = graph._replace(node_features=graph.node_features[0])
        self._clusters = self._clustering_algorithm.run(graph) if self._clusters is None else self._clusters
        # clusters = [x.to(device) for x in clusters]
        # graph = self._graph_to_device(graph._replace(node_features=graph.node_features[0]), device)
        new_graph = self._node_connector.run(graph, self._clusters, is_training)

        return new_graph

    def reset_clusters(self):
        """
        Reset the current clustering structure and therefore force its recomputation
        on the next call of :func:`RemoteMessagePassing.create_graph`
        """
        self._clusters = None

    @staticmethod
    def _graph_to_device(graph, dev):
        return MultiGraphWithPos(node_features=graph.node_features.to(dev),
                                 edge_sets=[EdgeSet(name=e.name,
                                                    features=e.features.to(dev),
                                                    senders=e.senders.to(dev),
                                                    receivers=e.receivers.to(dev)) for e in graph.edge_sets],
                                 target_feature=graph.target_feature.to(dev),
                                 model_type=graph.model_type,
                                 node_dynamic=graph.node_dynamic.to(dev))
