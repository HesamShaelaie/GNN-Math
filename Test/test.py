

import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
ox.folium.plot_graph_folium(ox.graph_from_place('Bethlehem, PA, USA', network_type = 'drive')).save('Bethlehem.html') 

