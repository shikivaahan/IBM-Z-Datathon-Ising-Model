import pandas as pd
import networkx as nx
import community as community_louvain

def detect_communities_louvain(G: nx.Graph) -> nx.Graph:
    """
    Performs Louvain community detection on a graph G and adds the community as a node attribute.
    
    Parameters:
    - G: nx.Graph, the graph on which to perform Louvain community detection.
    
    Returns:
    - G: nx.Graph, the graph with community information added as a node attribute.
    """
    # Perform Louvain community detection
    partition = community_louvain.best_partition(G)
    
    # Assign community to each node as an attribute
    nx.set_node_attributes(G, partition, 'community')
    
    return G