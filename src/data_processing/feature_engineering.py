import pandas as pd
import networkx as nx

def add_labels_to_graph(G: nx.Graph, df: pd.DataFrame, label_col: str) -> nx.Graph:
    """
    Adds labels from a DataFrame to the nodes in the graph G.
    If a node already has a label, the new label is appended to the existing labels.
    
    Parameters:
    G (networkx.Graph): The graph to which labels will be added.
    df (pandas.DataFrame): The DataFrame containing labels.
    label_col (str): The name of the column in df that contains the labels.
    
    Returns:
    networkx.Graph: The updated graph with labels added to nodes.
    """
    for index, row in df.iterrows():
        node_id = row['node_column_name']  # Replace with the actual node ID column name
        new_label = row[label_col]

        # If the node already has a label, append the new label
        if G.has_node(node_id):
            if 'label' in G.nodes[node_id]:
                existing_labels = G.nodes[node_id]['label']
                # Ensure we don't append the same label again
                if new_label not in existing_labels:
                    existing_labels.append(new_label)
                G.nodes[node_id]['label'] = existing_labels
            else:
                G.nodes[node_id]['label'] = [new_label]  # Initialize label as a list
        else:
            G.add_node(node_id, label=[new_label])  # Create a new node with label

    return G