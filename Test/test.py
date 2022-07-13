
import osmnx as ox

import matplotlib.pyplot as plt
g = ox.graph.graph_from_address("Bethelehem, PA")
nx.draw(g)
plt.show()

