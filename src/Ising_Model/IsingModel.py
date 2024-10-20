import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

class IsingModel:
    """
    A class to simulate the Ising model on a given graph using Monte Carlo methods.

    Attributes:
        graph (networkx.Graph): The input graph representing the social network.
        n_nodes (int): The number of nodes in the graph.
        spins (numpy.ndarray): An array representing the spin states of the nodes.
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

    def calculate_energy(self):
        """
        Calculate the total energy of the Ising model for the current spin configuration.

        Returns:
            float: The total energy of the system.
        """
        energy = 0
        edges = np.array(self.graph.edges())
        
        for edge in edges:
            s1 = self.spins[edge[0]]
            s2 = self.spins[edge[1]]
            energy -= s1 * s2  # Interaction energy
            
        return energy

    def calculate_magnetization(self):
        """
        Calculate the total magnetization of the Ising model.

        Returns:
            float: The total magnetization of the system.
        """
        return np.sum(self.spins)

    def flip_spin(self, node):
        """
        Flip the spin of the specified node in the graph.

        Args:
            node (int): The node index whose spin is to be flipped.
        """
        self.spins[node] *= -1

    def monte_carlo_step(self, temperature):
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

    def simulate(self, temperatures, steps_per_temperature):
        """
        Simulate the Ising model for a range of temperatures and return energy and magnetization data.

        Args:
            temperatures (list or ndarray): A list or array of temperatures to simulate.
            steps_per_temperature (int): The number of Monte Carlo steps for each temperature.

        Returns:
            tuple: A tuple of three lists: 
                - energy_data: The average energy at each temperature.
                - magnetization_data: The average magnetization at each temperature.
                - correlation_data: The average spin values (correlations) at each temperature.
        """
        energy_data = []
        magnetization_data = []
        correlation_data = []

        for temp in temperatures:
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
    def plot_quantity_vs_temperature(quantity_data, temperatures, quantity_name):
        """
        Plot a physical quantity (e.g., energy, magnetization) against temperature.

        Args:
            quantity_data (list): A list of average quantity values for each temperature.
            temperatures (list or ndarray): A list or array of temperatures.
            quantity_name (str): The name of the quantity to plot.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(temperatures, quantity_data, marker='o')
        plt.title(f'{quantity_name} vs Temperature')
        plt.xlabel('Temperature')
        plt.ylabel(quantity_name)
        plt.grid(True)
        plt.show()

