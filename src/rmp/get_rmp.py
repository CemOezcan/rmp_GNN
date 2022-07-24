"""
Utility class to select a remote message passing strategy based on a given config file
"""
from src.rmp.hdbscan import HDBSCAN
from src.rmp.hierarchical_connector import HierarchicalConnector
from src.rmp.multigraph_connector import MultigraphConnector
from src.rmp.random_clustering import RandomClustering
from util.Types import *
from src.rmp.remote_message_passing import RemoteMessagePassing
from src.rmp.abstract_clustering_algorithm import AbstractClusteringAlgorithm
from src.rmp.abstract_connector import AbstractConnector

from util.Functions import get_from_nested_dict


def get_rmp(config: ConfigDict) -> RemoteMessagePassing:
    # TODO: Change config template to fit the following
    clustering_name = get_from_nested_dict(config, list_of_keys=["rmp", "clustering"], raise_error=True).lower()
    connector_name = get_from_nested_dict(config, list_of_keys=["rmp", "connector"], raise_error=True).lower()

    clustering = get_clustering_algorithm(clustering_name)
    connector = get_connector(connector_name)

    return RemoteMessagePassing(clustering, connector)


def get_clustering_algorithm(name: str) -> AbstractClusteringAlgorithm:
    if name == "hdbscan":
        return HDBSCAN()
    elif name == "random":
        return RandomClustering()
    elif name == "none":
        return None
    else:
        raise NotImplementedError("Implement your clustering algorithms here!")


def get_connector(name: str) -> AbstractConnector:
    if name == "hierarchical":
        return HierarchicalConnector()
    elif name == "multigraph":
        return MultigraphConnector()
    elif name == "none":
        return None
    else:
        raise NotImplementedError("Implement your connectors here!")
