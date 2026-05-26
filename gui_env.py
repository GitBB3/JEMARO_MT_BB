import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import networkx as nx
import numpy as np

from environment import Environment

def DisplayEnvironment(env):
    """
    Display the environment.
    """
    adjacency_matrix = env.adjacencyMat
    ## Creating a graph
    G = nx.from_numpy_array(adjacency_matrix)
    ## Optimizing the position of the hexagons
    pos = nx.spring_layout(G, k=1.5, iterations=150, seed=42) #k controling the optimal distance between nodes
    ## Computation of the size of hexagons so that they can really be adjacent on the figure
    distances = [np.linalg.norm(pos[u] - pos[v]) for u, v in G.edges()]
    dist_moyenne = np.mean(distances) if distances else 1.0
    rayon = dist_moyenne / np.sqrt(3) # hexagon formula
    
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ## Drawing hexagons
    for node, coords in pos.items():
        x, y = coords
        hexagon = RegularPolygon(
            (x, y), 
            numVertices=6, 
            radius=rayon * 0.95, # leave some space between hexagons
            orientation=0, 
            edgecolor='black', 
            facecolor='#E6F2FF', 
            linewidth=1.5,
            zorder=2
        ) # hexagon
        ax.add_patch(hexagon)
        ax.text(
            x, y, str(node), 
            ha='center', va='center', 
            fontsize=11, fontweight='bold', color='navy',
            zorder=3
        ) # agent ID
    ## Drawing adjacence lines
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.plot([x1, x2], [y1, y2], color='gray', linestyle=':', alpha=0.6, zorder=1)
    ## Adjust the screen
    all_x = [c[0] for c in pos.values()]
    all_y = [c[1] for c in pos.values()]
    ax.set_xlim(min(all_x) - rayon, max(all_x) + rayon)
    ax.set_ylim(min(all_y) - rayon, max(all_y) + rayon)
    plt.axis('off')
    plt.title("Environment of PlaceAgents", fontsize=14)
    plt.show()

if __name__ == "__main__":
    # adjacency_matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 1],  # 0
    #     [0, 0, 1, 0, 0, 0, 1, 0],  # 1
    #     [0, 1, 0, 1, 0, 0, 0, 0],  # 2
    #     [0, 0, 1, 0, 1, 0, 0, 0],  # 3
    #     [0, 0, 0, 1, 0, 1, 0, 0],  # 4
    #     [0, 0, 0, 0, 1, 0, 1, 1],  # 5
    #     [0, 1, 0, 0, 0, 1, 0, 1],  # 6
    #     [1, 0, 0, 0, 0, 1, 1, 0]   # 7
    # ]
    env = Environment(np.zeros((6,6)))
    env.env_generator()
    DisplayEnvironment(env)