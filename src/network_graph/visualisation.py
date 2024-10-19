import networkx as nx
import matplotlib.pyplot as plt

def visualise_graph(G: nx.Graph, node_color='lightblue', node_size=500, with_labels=True, layout='spring'):
    """
    Visualizes the graph using NetworkX and Matplotlib.
    
    Parameters:
    - G: nx.Graph, the graph to be visualized.
    - node_color: str or list, color of the nodes.
    - node_size: int or list, size of the nodes.
    - with_labels: bool, whether to display node labels.
    - layout: str, the layout algorithm to use ('spring', 'circular', 'random', 'shell', etc.).
    """
    
    # Choose layout
    if layout == 'spring':
        pos = nx.spring_layout(G)  # Force-directed layout (good for most cases)
    elif layout == 'circular':
        pos = nx.circular_layout(G)  # Circular layout
    elif layout == 'random':
        pos = nx.random_layout(G)  # Random layout
    elif layout == 'shell':
        pos = nx.shell_layout(G)  # Shell layout
    else:
        pos = nx.spring_layout(G)  # Default to spring layout if unrecognized layout

    # Draw the graph
    plt.figure(figsize=(24, 18))  # You can adjust the figure size as needed
    nx.draw(
        G, pos, node_color=node_color, node_size=node_size, with_labels=with_labels, 
        font_size=10, font_color='black', font_weight='bold', edge_color='gray'
    )

    # Display the plot
    plt.title("Graph Visualization")
    plt.show()
