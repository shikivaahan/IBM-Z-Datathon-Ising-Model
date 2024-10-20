import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

class IsingModel:
    """
    A class to simulate the Ising model on a given graph using Monte Carlo methods.

    Attributes:
        graph (networkx.Graph): The input graph representing the social network.
        n_nodes (int): The number of nodes in the graph.
        spins (numpy.ndarray): An array representing the spin states of the nodes.
        node_to_index (dict): A mapping from node identifiers to their respective indices.
    """

    def __init__(self, graph):
        """
        Initializes the Ising model with a graph and assigns random spins.

        Args:
            graph (networkx.Graph): The graph on which to simulate the Ising model.
        """
        self.graph = graph
        self.n_nodes = len(graph.nodes())
        self.spins = np.random.choice([-1, 1], size=self.n_nodes)
        self.node_to_index = {node: i for i, node in enumerate(graph.nodes())}  # Create mapping

    def calculate_energy(self):
        """
        Calculate the total energy of the Ising model for the current spin configuration.

        Returns:
            float: The total energy of the system.
        """
        energy = 0
        edges = np.array(self.graph.edges())
        
        for edge in edges:
            # Use the mapping to get the index
            s1 = self.spins[self.node_to_index[edge[0]]]
            s2 = self.spins[self.node_to_index[edge[1]]]
            energy -= s1 * s2  # Interaction energy
            
        return energy

    def flip_spin(self, node):
        """
        Flip the spin of the specified node in the graph.

        Args:
            node: The node identifier whose spin is to be flipped.
        """
        index = self.node_to_index[node]  # Get index from mapping
        self.spins[index] *= -1

    def monte_carlo_step(self, temperature):
        """
        Perform a single Monte Carlo step using the Metropolis algorithm for the Ising model.

        Args:
            temperature (float): The temperature at which to perform the Monte Carlo step.
        """
        for node in self.graph.nodes():  # Iterate over nodes directly
            current_energy = self.calculate_energy()
            
            # Attempt to flip the spin
            self.flip_spin(node)
            new_energy = self.calculate_energy()
            
            # Calculate the energy change
            delta_energy = new_energy - current_energy
            
            # Accept or reject the flip based on Metropolis criterion
            if delta_energy > 0 and random.random() >= np.exp(-delta_energy / temperature):
                self.flip_spin(node)  # Flip back if not accepted

    def simulate(self, temperatures, steps_per_temperature):
        """
        Simulate the Ising model for a range of temperatures and return correlation data.

        Args:
            temperatures (list or ndarray): A list or array of temperatures to simulate.
            steps_per_temperature (int): The number of Monte Carlo steps for each temperature.

        Returns:
            list: A list of average spin values (correlations) for each temperature.
        """
        correlation_data = []

        for temp in temperatures:
            self.spins = np.random.choice([-1, 1], size=self.n_nodes)  # Reset spins for each temperature
            
            # Use tqdm to create a progress bar for the Monte Carlo steps
            for _ in tqdm(range(steps_per_temperature), desc=f'Simulating at T={temp}'):
                self.monte_carlo_step(temp)
                
            # Calculate the correlation of spins
            correlation = np.mean(self.spins)  # Average spin can represent correlation
            correlation_data.append(correlation)
        
        return correlation_data

    @staticmethod
    def plot_correlation_vs_temperature(correlation_data, temperatures):
        """
        Plot the correlation against temperature.

        Args:
            correlation_data (list): A list of average spin values for each temperature.
            temperatures (list or ndarray): A list or array of temperatures.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(temperatures, correlation_data, marker='o')
        plt.title('Correlation vs Temperature')
        plt.xlabel('Temperature')
        plt.ylabel('Correlation')
        plt.grid(True)
        plt.show()