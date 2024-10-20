import pandas as pd
import networkx as nx
from typing import Tuple

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

def add_edge_attributes(G: nx.Graph, edge_col: Tuple[str, str], attribute_col: str, df: pd.DataFrame) -> nx.Graph:
    """
    Adds attributes (e.g., timestamps) to edges in a graph G based on edge_col and attribute_col from a DataFrame.
    If the attribute already exists for the edge, it appends the new attribute to a list.
    
    Parameters:
    - G: nx.Graph, the graph to which attributes will be added.
    - edge_col: tuple of str, the two columns in the DataFrame representing the source and target nodes of the edges.
    - attribute_col: str, the column in the DataFrame representing the attributes (e.g., timestamps) to assign to edges.
    - df: pd.DataFrame, the DataFrame containing edge and attribute data.
    
    Returns:
    - G: nx.Graph, the graph with appended edge attributes.
    """
    
    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        node1 = row[edge_col[0]]
        node2 = row[edge_col[1]]
        attribute = row[attribute_col]
        
        # Check if the edge exists in the graph
        if G.has_edge(node1, node2):
            # If the edge already has the attribute, append it to the list
            if attribute_col in G.edges[node1, node2]:
                if isinstance(G.edges[node1, node2][attribute_col], list):
                    # Append to the list if the attribute is already a list
                    G.edges[node1, node2][attribute_col].append(attribute)
                else:
                    # Convert the existing attribute to a list and append the new one
                    G.edges[node1, node2][attribute_col] = [G.edges[node1, node2][attribute_col], attribute]
            else:
                # If the attribute doesn't exist, add it as a single item
                G.edges[node1, node2][attribute_col] = [attribute]
    
    return G


def export_graph_to_csv(graph: nx.Graph, nodes_file: str = 'nodes.csv', edges_file: str = 'edges.csv') -> None:
    """
    Export the nodes and edges of a NetworkX graph to CSV files.

    Parameters:
    - graph (nx.Graph): The input graph to be exported.
    - nodes_file (str): The filename or path for the nodes CSV file. Defaults to 'nodes.csv'.
    - edges_file (str): The filename or path for the edges CSV file. Defaults to 'edges.csv'.

    Returns:
    - None: This function does not return any value. It writes the nodes and edges to CSV files.

    The nodes CSV will include each node's identifier and its associated attributes as columns. 
    If a node does not have a specific attribute, that column will contain NaN values.
    
    The edges CSV will include the source and target nodes for each edge, the datetime, and any associated edge attributes.
    """
    # Export nodes with attributes
    nodes_data = []
    for node, attrs in graph.nodes(data=True):
        node_data = {'node': node}
        node_data.update(attrs)  # Add node attributes if available
        nodes_data.append(node_data)
    
    # Convert nodes data to a pandas DataFrame and ensure all attributes are columns
    nodes_df = pd.DataFrame(nodes_data)
    
    # Fill missing values with NaN
    nodes_df = nodes_df.fillna(value=pd.NA)
    
    # Export nodes to CSV
    nodes_df.to_csv(nodes_file, index=False)

    # Export edges with attributes including datetime
    edges_data = []
    for u, v, attrs in graph.edges(data=True):
        edge_data = {
            'source': u,
            'target': v,
            'datetime': attrs.get('datetime')  # Add 'datetime' if it exists, otherwise None
        }
        edge_data.update(attrs)  # Add other edge attributes if available
        edges_data.append(edge_data)

    # Convert edges data to a pandas DataFrame
    edges_df = pd.DataFrame(edges_data)
    
    # Fill missing values with NaN
    edges_df = edges_df.fillna(value=pd.NA)

    # Export edges to CSV
    edges_df.to_csv(edges_file, index=False)

    print(f'Graph exported: {nodes_file} (nodes), {edges_file} (edges with datetime)')


