import matplotlib.pyplot as plt
import networkx as nx

def visualise_graph(G: nx.Graph, color_by: str = 'label', node_size: int = 500, 
                    with_labels: bool = True, layout: str = 'spring') -> None:
    """
    Visualizes the graph using NetworkX and Matplotlib, coloring nodes based on a specified attribute.

    Parameters:
    - G (nx.Graph): The graph to be visualized.
    - color_by (str, optional): Attribute to color the nodes by. 
                                 Options are 'label' (coloring based on label values) or 
                                 'community' (coloring based on community assignment). 
                                 Default is 'label'.
    - node_size (int, optional): Size of the nodes. Default is 500.
    - with_labels (bool, optional): Whether to display node labels. Default is True.
    - layout (str, optional): The layout algorithm to use for positioning the nodes. 
                              Options include 'spring', 'circular', 'random', 'shell', etc. 
                              Default is 'spring'.

    Returns:
    - None: This function displays the graph visualization and does not return any value.
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

    # Determine node colors based on the specified attribute
    if color_by == 'label':
        node_color = ['green' if G.nodes[node].get('label', [0])[0] == 1 else 'red' for node in G.nodes()]
    elif color_by == 'community':
        # Assign a unique color to each community
        communities = {community: idx for idx, community in enumerate(set(nx.get_node_attributes(G, 'community').values()))}
        # Get the number of unique communities to define the colormap
        num_communities = len(communities)
        colormap = plt.cm.tab10  # Use the tab10 colormap
        
        # Assign colors based on the community index
        node_color = [colormap(idx % num_communities) for node in G.nodes() for idx in [communities[G.nodes[node].get('community', 0)]]]
    else:
        node_color = 'lightblue'  # Default color if unrecognized attribute

    # Draw the graph
    plt.figure(figsize=(24, 18))  # You can adjust the figure size as needed
    nx.draw(
        G, pos, node_color=node_color, node_size=node_size, with_labels=with_labels, 
        font_size=10, font_color='black', font_weight='bold', edge_color='gray'
    )

    # Display the plot
    plt.title("Graph Visualization")
    plt.show()
