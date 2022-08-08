from functools import cache
import osmnx as ox
import networkx as nx
import plotly.graph_objects as go
import numpy as np

'''
G = ox.graph_from_place('Belgrade, Serbia')
ox.plot_graph(G)



G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
G_projected = ox.project_graph(G)
ox.plot_graph(G_projected)

'''

G = ox.graph_from_place('San Jose, United States', network_type="drive")
ox.save_graph_geopackage(G, filepath="/Users/hesamshaelaie/Documents/Research/GNN-Math/Maps/piedmont.gpkg")

#ox.plot_graph(G)


origin_point = (37.335022,-121.935522)
destination_point = (37.362706,-121.889426)

origin_node = ox.nearest_nodes(G, origin_point)
destination_node = ox.nearest_nodes(G, destination_point)


#print(origin_node)
#print(destination_node)

route = nx.shortest_path(G, origin_node, destination_node, weight='length')
fig, ax = ox.plot_graph_route(G, route, origin_point=origin_point, destination_point=destination_point)


