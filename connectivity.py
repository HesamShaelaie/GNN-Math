# A class to represent a graph object
class Graph:

    # Constructor
    def __init__(self, edges, n):
 
        # A list of lists to represent an adjacency list
        self.adjList = [[] for _ in range(n)]

        # add edges to the directed graph
        for (src, dest) in edges:
            self.adjList[src].append(dest)


# Function to perform DFS traversal on the graph on a graph
def DFS(graph, v, visited):

    # mark current node as visited
    visited[v] = True
 
    # do for every edge (v, u)
    for u in graph.adjList[v]:
        # `u` is not visited
        if not visited[u]:
            DFS(graph, u, visited)
 
 
# Check if the graph is strongly connected or not
def isStronglyConnected(graph, n):
 
    # do for every vertex
    for i in range(n):
 
        # to keep track of whether a vertex is visited or not
        visited = [False] * n
 
        # start DFS from the first vertex
        DFS(graph, i, visited)
 
        # If DFS traversal doesn't visit all vertices,
        # then the graph is not strongly connected
        for b in visited:
            if not b:
                return False
 
    return True
 
 
if __name__ == '__main__':
 
    # List of graph edges as per the above diagram
    edges = [(0, 4), (1, 0), (1, 2), (2, 1), (2, 4), (3, 1), (3, 2), (4, 3), (5,6)]
 
    # total number of nodes in the graph
    n = 7
 
    # construct graph
    graph = Graph(edges, n)
 
    # check if the graph is not strongly connected or not
    if isStronglyConnected(graph, n):
        print('The graph is strongly connected')
    else:
        print('The graph is not strongly connected')