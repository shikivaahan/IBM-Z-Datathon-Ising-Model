import networkx as nx
import pandas as pd

def process_nodes(G: nx.Graph, df: pd.DataFrame, node_col: str, label_col: str) -> nx.Graph:
    """
    Assigns spin values to the nodes in the graph G based on a DataFrame.
    
    Parameters:
    - G: nx.Graph, the graph to which spin values will be added.
    - df: pd.DataFrame, the DataFrame containing node and spin data.
    - node_col: str, the column in the DataFrame representing the nodes.
    - spin_col: str, the column in the DataFrame representing the spin values to assign to nodes.
    
    Returns:
    - G: nx.Graph, the graph with assigned spin values as node attributes.
    """
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        node = row[node_col]
        label_value = row[label_col]
        
        # Check if the node exists in the graph
        if node in G:
            # Assign the spin value as an attribute to the node
            G.nodes[node]['spin'] = label_value
    
    return G