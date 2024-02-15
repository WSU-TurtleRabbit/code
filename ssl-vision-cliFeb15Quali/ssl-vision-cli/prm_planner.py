
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import numpy as np

class PRMPlanning:
    def __init__(self, xy_min, xy_max):
        self.xy_min = xy_min  # Field minimum dimensions in millimeters
        self.xy_max = xy_max  # Field maximum dimensions in millimeters

    def populate_graph(self, obstacles, num_samples, radius):
        samples = np.random.uniform(low=self.xy_min, high=self.xy_max, size=(num_samples, 2))
        graph = nx.Graph()

        for sample in samples:
            sample_tuple = tuple(sample)
            if not self.is_obstacle(obstacles, sample_tuple):
                graph.add_node(sample_tuple)

        knn = NearestNeighbors(radius=radius)
        knn.fit(samples)

        for sample in samples:
            sample_tuple = tuple(sample)
            indices = knn.radius_neighbors([sample], radius=radius, return_distance=False)[0]
            for index in indices:
                neighbor_tuple = tuple(samples[index])
                if not self.is_obstacle(obstacles, neighbor_tuple) and sample_tuple != neighbor_tuple:
                    graph.add_edge(sample_tuple, neighbor_tuple)

        return graph

    def find_path(self, graph, start, end):
        start_tuple, end_tuple = tuple(start), tuple(end)
        if start_tuple in graph and end_tuple in graph:
            path = nx.shortest_path(graph, source=start_tuple, target=end_tuple, weight=None)
            return path
        else:
            raise ValueError("Start or end point not in graph.")

    def is_obstacle(self, obstacles, point):
        for obstacle in obstacles:
            if np.linalg.norm(np.array(obstacle) - np.array(point)) < 500:  # 500mm considered as a buffer zone around obstacles
                return True
        return False