#!/bin/python3

import sys

class Graph(object):

    ###########################################################################
    ## UTILITY FUNCTIONS  
    ###########################################################################

    def __init__(self, N, matrix=False, directed=False):
        # initiate graph class with number of nodes, N
        # by default use adjacency list representation
        # matrix indicates an adjacency matrix will be used
        # directed indicates whether the graph is directed

        # get directives
        self.N = N
        self.M = 0
        self.matrix = matrix
        self.directed = directed
        
        # set up graph representation
        if(self.matrix):
            self.G = [[None]*N for i in range(N)]
        else:
            self.G = {key : set([]) for key in range(N)}
            self.W = {}

    def add_edge(self, i, j, w, override=False):
        # add edge between i and j with weight w
        # in matrix representation, i and j are assumed to be zero indexed
        
        if(self.matrix):
            if(self.G[i][j] != None and self.G[i][j] < w):
                return
            self.G[i][j] = w
            if(not self.directed): # FIXME this will break some things
                self.G[i][j] = w
        else:
            # check if there is already a connection from i to j.
            # if we have a duplicate, keep the cheaper option
            if(i in self.G and j in self.G[i]):                
                self.W[i][j] = w if self.W[i][j] > w  or override else self.W[i][j]
            else:
                self.M += 1
                self.G[i].add(j)
                if(i in self.W):
                    self.W[i][j] = w
                else:
                    self.W[i] = {j : w}
                
            # add the second node if undirected
            if(not self.directed):
                if(j in self.G and i in self.G[j]):                
                    self.W[j][i] = w if self.W[j][i] > w or override else self.W[j][i]
                else:
                    self.G[j].add(i)                
                    if(j in self.W):
                        self.W[j][i] = w
                    else:
                        self.W[j] = {i : w}
                
                
    ###########################################################################
    ## OBJECTIVE FUNCTIONS  
    ###########################################################################

    def is_spanning(self):
        # determines if self is spanning.
        if(self.matrix):
            for node1 in range(self.N):
                connected = False
                for node2 in range(i+1, self.N):
                    if(self.G[node1][node2] != None):
                        connected = True
                        break
                if(not connected):
                    return False
        else:
            for node1 in self.W:
                if(len(self.W[node1]) == 0): 
                    return False
        return True

    def get_neighbors(self, i):
        # returns the neighbors belonging to node i
        # returns a list of nodes
        if(self.matrix):
            return [ind for ind, i in enumerate(self.G[i]) if i != None]
        else:
            return self.G[i]                
                       
    def get_component(self, i):
        # returns all nodes in a a component to which i belongs
        # effectively performs a DFS!
        visited = set([])
        frontier = [i]
        while(len(frontier)):
            node = frontier.pop()
            if(not (node in visited)):
                visited.add(node)
                for neighbor in self.get_neighbors(node):
                    if(neighbor in visited):
                        continue
                    else:
                        frontier.append(neighbor)
        return visited

    def MST_Prim_weight(self):
        # Modified Prim's algorithm 
        # returns MST weight, not actual MST graph
        N = self.N
        M = self.M
        Q = set([_ for _ in range(N)])
        C = {key : float('inf') for key in range(N)}
        if(self.matrix):
            while (len(Q)):
                val, ind = min((C[j], j) for j in Q)
                Q.remove(ind)
                W = [j for j in range(N) if self.G[ind][j] != None]
                for w in W:
                    if ((w in Q) and (self.G[ind][w] < C[w])):
                        C[w] = self.G[ind][w]
        else:
            while (len(Q)):
                val, ind = min((C[j], j) for j in Q)
                Q.remove(ind)
                W = self.G[ind]
                for w in W:
                    if ((w in Q) and (self.W[ind][w] < C[w])):
                        C[w] = self.W[ind][w]
        return sum(_ for _ in C.values() if _ != float('inf'))

    def MST_Kruskal_weight(self):
        # Modified Kruskal's algorithm 
        # returns MST weight and MST graph
        
        # create empty graph with N trees
        new_graph = Graph(self.N)
        
        # construct a list of edges (node1, node2, weight)
        S = []
        if(self.matrix):
            for node1 in range(self.N):
                for node2 in range(i+1, self.N):
                    if(self.G[node1][node2] != None):
                        S.append([node1, node2, self.G[node1][node2]])
        else:
            for node1 in self.W:
                for node2 in self.W[node1]:
                    if(node1 < node2):
                        S.append([node1, node2, self.W[node1][node2]])

        # sort the edges by weight
        S.sort(key=lambda x: x[2])         
            
        total_weight = 0
        while(S and new_graph.is_spanning):
            
            node1, node2, weight = S.pop(0)
            connected_nodes = new_graph.bfs(node1)
            if(node2 in connected_nodes):
                continue
            else:
                new_graph.add_edge(node1, node2, weight)
                total_weight += weight
        
        return total_weight, new_graph 

    def get_subgraph(self, nodes, matrix=False):
        # generates a subgraph from a subset of nodes
        n = len(nodes)
        if(n == 0):
            return Graph(1)
        nodes.sort()
        new_graph = Graph(len(nodes))
        if(matrix):
            for ind1, i in enumerate(nodes):
                for ind2, j in enumerate(nodes[ind1+1:]):
                    if(self.G[i][j] != None):
                        new_graph.add_edge(ind1, ind2 + ind1 + 1, self.G[i][j])
        else:
            ind_map = {key : val for val, key in enumerate(nodes)}
            for i in self.G:
                for j in self.G[i]:
                    new_graph.add_edge(ind_map[i], ind_map[j], self.W[i][j])
        return new_graph
 

    def get_connected_component_counts(self):
        # returns counts, an array of length = # of components
        # each element in counts dictates the size of a component
        # the function is not stable with regard to counts, it can
        # come out in any order, since set.pop() is used. But the number
        # of components and size of each component is consistent
        counts = []
        to_visit = set([_ for _ in range(self.N)])
        while(len(to_visit)):
            component = self.get_component(to_visit.pop()) 
            to_visit.difference_update(component)
            counts.append(len(component))
        return counts

    
    def bfs(self, i):
        from collections import deque
        # params: i - node
        # return a list from 0 to n-1 containing shortest distances to i
        # returns all reachable nodes (component) from node i
        # the return is a dictionary key: reachable node, val: cost
        visited = {}
        frontier = deque()
        frontier.append([i, 0])
        while(len(frontier)):
            node, cost = frontier.popleft()
            if(not (node in visited)):
                visited[node] = cost
                for neighbor in self.get_neighbors(node):
                    if(neighbor in visited):
                        continue
                    else:
                        frontier.append([neighbor, cost + self.W[node][neighbor]])
        return visited
    
    def dijkstras_total(self, s):
        # disjkstras is a total uniform cost search
        
        # setup ~        
        distances = [float('inf')] * self.N
        frontier = PriorityQueue(heap=True)
        frontier.push((0, s))
        visited = set([-1])
                
        # loop
        current_node = -1
        while(frontier.n != 0):

            # get current node
            while(frontier.n != 0 and current_node in visited):
                cost, current_node = frontier.pop()
            
            if(current_node in visited):
                break
            
            distances[current_node] = cost
            visited.add(current_node)
            
            # get all neighbors,     
            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if(not neighbor in visited):
                    frontier.push((cost + self.W[current_node][neighbor], neighbor))
            
        return distances
    
    def floydWarshall_total_total(self):
        # Floyd-Warshall algorithm for finding minimum distance of every
        # node to every other node. 
        # computational: O(V^3)
        # space: O(V^2)
        # assumes nodes are zero indexed!
        
        # setup ~
        distances = [[float('inf')] * self.N for _ in range(self.N)]
        for i in range(self.N):
            distances[i][i] = 0
        for node1 in self.W:
            for node2 in self.W[node1]:
                distances[node1][node2] = self.W[node1][node2]
            
        for k in range(self.N):
            for i in range(self.N):
                for j in range(self.N):
                    if(distances[i][j] > distances[i][k] + distances[k][j]):
                        distances[i][j] = distances[i][k] + distances[k][j]
        return distances

from heapq import heappush
from heapq import heappop
class PriorityQueue(object):
    
    def __init__(self, heap=False):
        self.n = 0
        self.heap = heap
        if(self.heap):
            self.queue = []
        else:
            self.queue = []
            self.current_nodes = set([])    
        
    def push(self, node):
        # when you push a node, assume that it is a tuple
        # the last element of the tuple is the primary key
        # the first element of the tuple is the cost 
        # do not use a heapq if you plan to push nodes in 
        # which the primary key already exists within the queue.
        # deleting nodes from a heapq is troublesome, use the
        # list implementation instead.
        if(self.heap):
            heappush(self.queue, node)
            self.n += 1
        else:
            node_identity = node[-1]
            if(node_identity in self.current_nodes):
                for ind, i in enumerate(self.queue):
                    if(i[-1] == node_identity):
                        pos = ind
                        break
                if(self.queue[pos][0] > node[0]):
                    self.queue.pop(pos)
                    pushed = False
                    for ind, i in enumerate(self.queue):
                        if(node[0] < i[0]):
                            self.queue.insert(ind, node)
                            pushed = True
                            break
                    if(not pushed):
                        self.queue.append(node)
                else:
                    pass
            else:
                self.n += 1
                pushed = False
                for ind, i in enumerate(self.queue):
                    if(node[0] < i[0]):
                        self.queue.insert(ind, node)
                        pushed = True
                        break
                if(not pushed):
                    self.queue.append(node)
                self.current_nodes.add(node[-1])
            
    def pop(self):
        self.n -= 1
        if(self.heap):
            return heappop(self.queue)
        else:
            self.current_nodes.remove(self.queue[0][-1])
            return self.queue.pop(0)


