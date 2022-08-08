import osmnx as ox

G = ox.graph_from_place('Belgrade, Serbia')
ox.plot_graph(G)



G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
G_projected = ox.project_graph(G)
ox.plot_graph(G_projected)