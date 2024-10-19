import networkx as nx
import pandas as pd

def create_graph(source_col: str, target_col: str, df: pd.DataFrame) -> nx.Graph:
    # Create an empty graph
    """
    Creates a graph from a DataFrame, where source_col and target_col represent the edges in the graph.
    
    Parameters:
    - source_col: str, the column in the DataFrame representing the source of each edge.
    - target_col: str, the column in the DataFrame representing the target of each edge.
    - df: pd.DataFrame, the DataFrame containing edge data.
    
    Returns:
    - nx.Graph, the graph created from the DataFrame.
    """
    graph = nx.Graph()

    # Iterate over the DataFrame rows and add edges between the source and target columns
    for _, row in df.iterrows():
        source = row[source_col]
        target = row[target_col]
        
        # Add an edge between the source and target
        graph.add_edge(source, target)
    
    return graph


def add_node_attributes(G: nx.Graph, node_col: str, attribute_col: str, df: pd.DataFrame) -> nx.Graph:
    """
    Adds attributes to nodes in a graph G based on node_col and attribute_col from a DataFrame.
    If the attribute already exists for the node, it appends the new attribute to a list.
    
    Parameters:
    - G: nx.Graph, the graph to which attributes will be added.
    - node_col: str, the column in the DataFrame representing the nodes.
    - attribute_col: str, the column in the DataFrame representing the attributes to assign to nodes.
    - df: pd.DataFrame, the DataFrame containing node and attribute data.
    
    Returns:
    - G: nx.Graph, the graph with appended node attributes.
    """
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        node = row[node_col]
        attribute = row[attribute_col]
        
        # Check if the node exists in the graph
        if node in G:
            # If the node already has the attribute, append it to the list
            if attribute_col in G.nodes[node]:
                if isinstance(G.nodes[node][attribute_col], list):
                    # Append to the list if the attribute is already a list
                    G.nodes[node][attribute_col].append(attribute)
                else:
                    # Convert the existing attribute to a list and append the new one
                    G.nodes[node][attribute_col] = [G.nodes[node][attribute_col], attribute]
            else:
                # If the attribute doesn't exist, add it as a single item
                G.nodes[node][attribute_col] = [attribute]
    
    return G

