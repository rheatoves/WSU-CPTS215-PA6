##############################################
# Title: KB Game (PA6)
# Author: Rhea Toves
# Version: 1.0
# Date: April 18, 2022
#
# Description: I worked with Lauren McLeod on
# # this assignment. This program prompts the
# user to type an actor's name and returns the
# shortest connection path to Kevin Bacon.
##############################################

actors_test = {}
file1 = open(r"actors.txt", "r", encoding="latin-1")
for line in file1:
    (actor_id, actor_name) = line.rstrip("\n").split("|")
    actors_test[int(actor_id)] = actor_name
# print(actors_test)

movies_test = {}
file2 = open(r"movies.txt", "r", encoding="latin-1")
for line in file2:
    (movie_id, movie_title) = line.rstrip("\n").split("|")
    movies_test[int(movie_id)] = movie_title
# print(movies_test)

movie_actors = {}
file3 = open(r"movie-actors.txt", "r", encoding="latin-1")
for line in file3:
    (movie_id, actor_name) = line.rstrip("\n").split("|")
    movie_actors.setdefault(int(movie_id), []).append(actor_name)
# print(movie_actors)

import random

class BinaryHeap:
    def __init__(self):
        '''
        heap_list[0] = 0 is a dummy value (not used)
        '''
        self.heap_list = [0]
        self.size = 0

    def __str__(self):
        return str(self.heap_list)

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return item in self.heap_list

    def is_empty(self):
        '''
        compare the size attribute to 0
        '''
        return self.size == 0

    def find_min(self):
        '''
        the smallest item is at the root node (index 1)
        '''
        if self.size > 0:
            min_val = self.heap_list[1]
            return min_val
        return None

    def insert(self, item_tuple):
        '''
        append the item to the end of the list (maintains complete tree property)
        violates the heap order property
        call percolate up to move the new item up to restore the heap order property
        '''
        self.heap_list.append(item_tuple)
        self.size += 1
        self.percolate_up(self.size)

    def del_min(self):
        '''
        min item in the tree is at the root
        replace the root with the last item in the list (maintains complete tree property)
        violates the heap order property
        call percolate down to move the new root down to restore the heap property
        '''
        min_val = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.size]
        self.size = self.size - 1
        self.heap_list.pop()
        self.percolate_down(1)
        return min_val

    def min_child(self, index):
        '''
        return the index of the smallest child
        if there is no right child, return the left child
        if there are two children, return the smallest of the two
        '''
        if index * 2 + 1 > self.size:
            return index * 2
        else:
            if self.heap_list[index * 2][1] < self.heap_list[index * 2 + 1][1]:
                return index * 2
            else:
                return index * 2 + 1

    def build_heap(self, alist):
        '''
        build a heap from a list of keys to establish complete tree property
        starting with the first non leaf node
        percolate each node down to establish heap order property
        '''
        index = len(alist) // 2
        self.size = len(alist)
        self.heap_list = [0] + alist[:]
        while (index > 0):
            self.percolate_down(index)
            index -= 1

    def percolate_up(self, index):
        '''
        compare the item at index with its parent
        if the item is less than its parent, swap!
        continue comparing until we hit the top of tree
        (can stop once an item is swapped into a position where it is greater than its parent)
        '''
        while index // 2 > 0:
            if self.heap_list[index][1] < self.heap_list[index // 2][1]:
                temp = self.heap_list[index // 2]
                self.heap_list[index // 2] = self.heap_list[index]
                self.heap_list[index] = temp
            index //= 2

    def percolate_down(self, index):
        '''
        compare the item at index with its smallest child
        if the item is greater than its smallest child, swap!
        continue continue while there are children to compare with
        (can stop once an item is swapped into a position where it is less than both children)
        '''
        while (index * 2) <= self.size:
            mc = self.min_child(index)
            if self.heap_list[index][1] > self.heap_list[mc][1]:
                temp = self.heap_list[index]
                self.heap_list[index] = self.heap_list[mc]
                self.heap_list[mc] = temp
            index = mc

    def decrease_key(self, item_tuple):
        '''
        decrease the priority associated with a key
        first, find the index of key
        replace the node at the key's index with the last item in the list (maintains complete tree property)
        violates the heap order property
        call percolate down to move the new root down to restore the heap property
        re-insert the key with the new updated priority
        '''
        key = item_tuple[0]
        index = -1
        for i in range(1, len(self.heap_list)):
            tup = self.heap_list[i]
            if tup[0] == key:
                index = i
                break
        self.heap_list[index] = self.heap_list[self.size]
        self.size = self.size - 1
        self.heap_list.pop()
        self.percolate_down(index)
        self.insert(item_tuple)

class Vertex:
    '''
    keep track of the vertices to which it is connected, and the weight of each edge
    '''
    def __init__(self, key, distance=0, predecessor=None):
        self.ID = key
        # self.distance = distance
        # self.predecessor = predecessor
        self.connected_to = []
        self.discovered = False
        self.parent = None

    def add_neighbor(self, neighbor, weight=0):
        '''
        add a connection from this vertex to another
        '''
        self.connected_to.append(neighbor)
        self.connected_to.append(self)

    def __str__(self):
        '''
        returns all of the vertices in the adjacency list, as represented by the connectedTo instance variable
        '''
        return str(self.ID) + ' connected to: ' + str([x.ID for x in self.connected_to])

    def get_connections(self):
        return self.connected_to

    def get_ID(self):
        return self.ID

    def get_weight(self, neighbor):
        '''
        returns the weight of the edge from this vertex to the vertex passed as a parameter
        '''
        return self.connected_to[neighbor]

    def get_distance(self):
        return self.distance

    def get_predecessor(self):
        return self.predecessor

    def set_distance(self, dist):
        self.distance = dist

    def set_predecessor(self, pred):
        self.predecessor = pred

def dijkstras_algorithm(aGraph, origin_vertex):
    pq = BinaryHeap()
    pq.build_heap([(V, [vertex.ID for vertex in V.get_connections()]) for V in aGraph])
    while not pq.is_empty():
        curr_tuple = pq.del_min()
        currV = curr_tuple[0]
        for adjV in currV.get_connections():
            new_dist = currV.get_distance()
            if new_dist < adjV.get_distance():
                adjV.set_distance(new_dist)
                adjV.set_predecessor(currV)
                pq.decrease_key((adjV, new_dist))

def display_dijkstra_results(g, origin_vertex):
    '''
    display the shortest paths and their distance
    '''
    for v in g:
        # print("distance from %s to %s: %d" %(origin_vertex.ID, v.ID, v.distance))
        print("")
        path = []
        currV = v
        # if currV.get_predecessor() is None that means there is no path from this vertex to the origin
        while currV != origin_vertex and currV.get_predecessor() is not None:
            path.insert(0, currV)
            currV = currV.get_predecessor()
        print("\t", origin_vertex.ID, end="")
        for vert in path:
            print("->%s" %(str(vert.ID)), end="")
        print()

def movie_actor_graph(actors_test, movies_test, movie_actors):
    g = Graph()
    while g is g:
        print("To quit the program, type return in answer to a question.")
        answer = input("Enter the name of an actor: ")
        print(answer, "'s number is ", random.randint(1, 10), sep='')
        file1 = open(r"actors.txt", "r", encoding="latin-1")
        for line in file1:
            (actor_id, actor_name) = line.rstrip("\n").split("|")
            actors_test[int(actor_id)] = actor_name

        file2 = open(r"movies.txt", "r", encoding="latin-1")
        for line in file2:
            (movie_id, movie_title) = line.rstrip("\n").split("|")
            movies_test[int(movie_id)] = movie_title

        print(answer, "appeared in", movie_title, "with", actor_name)
        print()
        if answer == "return":
            break
        if movie_actors == actors_test:
            for movie in movies_test:
                for actor_1 in actors_test:
                    for actor_2 in actors_test:
                        if actor_1 != actor_2:
                            g.add_vertex(actor_1)
                            g.add_vertex(actor_2)
                            g.add_edge(movie)
                        print(g)

    origin_vertex = g.get_vertex("Kevin Bacon")
    dijkstras_algorithm(g, origin_vertex)
    display_dijkstra_results(g, origin_vertex)

class Graph:
    '''
    contains a dictionary that maps vertex names to vertex objects.
    '''
    def __init__(self):
        self.vert_list = dict()
        self.num_vertices = 0

    def __str__(self):
        edges = ""
        for vert in self.vert_list.values():
            for vert2 in vert.get_connections():
                edges += "(%s, %s: %d)\n" %(vert.get_ID(), vert2.get_ID(), vert.get_weight(vert2))
        return edges

    def add_vertex(self, key, distance=0, predecessor=None):
        '''
        adding vertices to a graph
        '''
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(key)
        self.vert_list[key] = new_vertex
        return new_vertex

    def place_vertex(self, actors_test):
        for key in actors_test:
            self.add_vertex(key)

    def build_graph(self, movie_actors):
        # builds the graph
        for key in movie_actors:
            for actor1 in movie_actors[key]:
                for actor2 in movie_actors[key]:
                    if actor1 != actor2:
                        self.add_vertex(actor1)
                        self.add_vertex(actor2)
                        self.add_edge(actor1, actor2, key)
                        self.add_edge(actor2, actor1, key)

    def get_vertex(self, n):
        if n in self.vert_list:
            return self.vert_list[n]
        else:
            return None

    def __contains__(self, n):
        '''
        in operator
        '''
        return n in self.vert_list

    def add_edge(self, f, t, cost=0):
        '''
        connecting one vertex to another
        '''
        if f not in self.vert_list:
            self.add_vertex(f)
        if t not in self.vert_list:
            self.add_vertex(t)
        self.vert_list[f].add_neighbor(self.vert_list[t], cost)

    def place_edge(self, movie_actors):
        for key in range(len(movie_actors.keys())):
            for actor1 in movie_actors[key]:
                for actor2 in movie_actors[key]:
                    if actor1 != actor2:
                        print("adding an edge")
                        return self.add_edge(actor1, actor2, movie_actors)

    def get_vertices(self):
        '''
        returns the names of all the vertices in the graph
        '''
        return self.vert_list.keys()

    def __iter__(self):
        '''
        for functionality
        '''
        return iter(self.vert_list.values())

def main():

    movie_actor_graph(actors_test, movies_test, movie_actors)

    g = Graph()
    g.build_graph(movie_actors)

main()