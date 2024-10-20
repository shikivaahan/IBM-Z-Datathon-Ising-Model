import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import List, Tuple
from tqdm import tqdm  # For the progress bar

class IsingModel:
    """
    A class to simulate the Ising model on a given graph using Monte Carlo methods.

    Attributes:
        graph (networkx.Graph): The input graph representing the social network.
        n_nodes (int): The number of nodes in the graph.
        spins (numpy.ndarray): An array representing the spin states of the nodes.
        node_to_idx (dict): A dictionary mapping graph nodes to integer indices.
        idx_to_node (dict): A dictionary mapping integer indices to graph nodes.
    """

    def __init__(self, graph: nx.Graph) -> None:
        """
        Initializes the Ising model with a graph and assigns random spins.

        Args:
            graph (networkx.Graph): The graph on which to simulate the Ising model.
        """
        self.graph = graph
        self.n_nodes = len(graph.nodes())

        # Create mappings between node labels and integer indices
        self.node_to_idx = {node: idx for idx, node in enumerate(graph.nodes())}
        self.idx_to_node = {idx: node for node, idx in self.node_to_idx.items()}

        self.spins = np.random.choice([-1, 1], size=self.n_nodes)

    def calculate_energy(self) -> float:
        """
        Calculate the total energy of the Ising model for the current spin configuration.

        Returns:
            float: The total energy of the system.
        """
        energy = 0
        edges = np.array(self.graph.edges())
        
        for edge in edges:
            # Get integer indices for the nodes
            s1 = self.spins[self.node_to_idx[edge[0]]]
            s2 = self.spins[self.node_to_idx[edge[1]]]
            energy -= s1 * s2  # Interaction energy
            
        return energy

    def calculate_magnetization(self) -> float:
        """
        Calculate the total magnetization of the Ising model.

        Returns:
            float: The total magnetization of the system.
        """
        return np.sum(self.spins)

    def flip_spin(self, node: int) -> None:
        """
        Flip the spin of the specified node in the graph.

        Args:
            node (int): The node index whose spin is to be flipped.
        """
        self.spins[node] *= -1

    def monte_carlo_step(self, temperature: float) -> None:
        """
        Perform a single Monte Carlo step using the Metropolis algorithm for the Ising model.

        Args:
            temperature (float): The temperature at which to perform the Monte Carlo step.
        """
        for node in range(self.n_nodes):
            current_energy = self.calculate_energy()
            
            # Attempt to flip the spin
            self.flip_spin(node)
            new_energy = self.calculate_energy()
            
            # Calculate the energy change
            delta_energy = new_energy - current_energy
            
            # Accept or reject the flip based on Metropolis criterion
            if delta_energy > 0 and random.random() >= np.exp(-delta_energy / temperature):
                self.flip_spin(node)  # Flip back if not accepted

    def simulate(self, temperatures: np.ndarray, steps_per_temperature: int) -> Tuple[List[float], List[float], List[float]]:
        """
        Simulate the Ising model for a range of temperatures and return energy, magnetization, and correlation data.

        Args:
            temperatures (np.ndarray): An array of temperatures to simulate.
            steps_per_temperature (int): The number of Monte Carlo steps for each temperature.

        Returns:
            Tuple: A tuple of three lists: 
                - energy_data (List[float]): The average energy at each temperature.
                - magnetization_data (List[float]): The average magnetization at each temperature.
                - correlation_data (List[float]): The average spin values (correlations) at each temperature.
        """
        energy_data = []
        magnetization_data = []
        correlation_data = []

        # Using tqdm for a progress bar
        for temp in tqdm(temperatures, desc="Simulating", unit="temperature"):
            self.spins = np.random.choice([-1, 1], size=self.n_nodes)  # Reset spins for each temperature
            
            for _ in range(steps_per_temperature):
                self.monte_carlo_step(temp)
            
            # Calculate the average energy, magnetization, and correlation
            avg_energy = self.calculate_energy() / self.n_nodes
            avg_magnetization = np.abs(self.calculate_magnetization()) / self.n_nodes
            avg_correlation = np.mean(self.spins)  # Average spin can represent correlation
            
            energy_data.append(avg_energy)
            magnetization_data.append(avg_magnetization)
            correlation_data.append(avg_correlation)
        
        return energy_data, magnetization_data, correlation_data

    @staticmethod
    def plot_quantity_vs_temperature(quantity_data: List[float], temperatures: np.ndarray, quantity_name: str) -> None:
        """
        Plot a physical quantity (e.g., energy, magnetization) against temperature.

        Args:
            quantity_data (List[float]): A list of average quantity values for each temperature.
            temperatures (np.ndarray): An array of temperatures.
            quantity_name (str): The name of the quantity to plot.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(temperatures, quantity_data, marker='o')
        plt.title(f'{quantity_name} vs Temperature')
        plt.xlabel('Temperature')
        plt.ylabel(quantity_name)
        plt.grid(True)
        plt.show()



