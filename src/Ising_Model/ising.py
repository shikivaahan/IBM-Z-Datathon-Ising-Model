import networkx as nx
import numpy as np

def ising_energy(graph, J=1.0):
    """
    Calculate the Ising energy of the graph. The energy function for each node
    will be influenced by the behavior (spin) of its neighbors.

    Parameters:
    graph (nx.DiGraph): A directed NetworkX graph where node values are either -1 or +1
                        representing negative and non-negative behavior respectively.
    J (float): Coupling constant (default 1.0), representing the interaction strength between users.

    Returns:
    dict: A dictionary of nodes with their corresponding energy values.
    """

    energy = {}
    
    for node in graph.nodes:
        node_behavior = graph.nodes[node]['behavior']  # Spin value of the node (-1 or +1)
        interaction_sum = 0
        
        # Iterate through neighbors
        for neighbor in graph.neighbors(node):
            interaction_sum += graph.nodes[neighbor]['behavior']  # Sum of neighbors' behaviors
        
        # Ising energy for node (simple pair interaction model)
        energy[node] = -J * node_behavior * interaction_sum
    
    return energy

def identify_susceptible_users(graph, J=1.0, threshold=0.5):
    """
    Identify users or communities that are highly susceptible to negative behavior.

    Parameters:
    graph (nx.DiGraph): A directed NetworkX graph where node values are either -1 or +1.
    J (float): Coupling constant representing the interaction strength.
    threshold (float): Threshold to identify high-susceptibility nodes (default is 0.5).

    Returns:
    dict: A dictionary containing susceptible nodes and their energy values.
    """
    energy_values = ising_energy(graph, J)
    
    # Identify nodes with energy values below the threshold (indicating high susceptibility)
    susceptible_nodes = {node: energy for node, energy in energy_values.items() if abs(energy) < threshold}
    
    return susceptible_nodes

def run_ising_model_analysis(graph, J=1.0, threshold=0.5):
    """
    Run the Ising model analysis on the graph and print values of interest.

    Parameters:
    graph (nx.DiGraph): A directed NetworkX graph where node values are either -1 or +1.
    J (float): Coupling constant representing the interaction strength (default is 1.0).
    threshold (float): Threshold to identify high-susceptibility nodes (default is 0.5).
    """

    # Step 1: Calculate energy values of all nodes based on the Ising model
    energy_values = ising_energy(graph, J)

    # Step 2: Identify highly susceptible nodes based on energy threshold
    susceptible_nodes = identify_susceptible_users(graph, J, threshold)

    # Output results
    print("Energy Values of Users:")
    for node, energy in energy_values.items():
        print(f"User {node}: Energy = {energy:.4f}")

    print("\nHighly Susceptible Users (Energy < Threshold):")
    for node, energy in susceptible_nodes.items():
        print(f"User {node}: Energy = {energy:.4f}")

