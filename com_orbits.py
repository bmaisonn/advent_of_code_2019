from collections import defaultdict

class OrbitGraph:
    """
    Direct graph describing object's orbit
    Adjacents objects are the objects which turn
    around the current vertex
    """
    def __init__(self, orbit_description_file_path):
        self.adjency_list = defaultdict(list)
        with open(orbit_description_file_path) as f:
            for l in f:
                center, orbiter = l.rstrip('\n').split(')')
                self.adjency_list[center].append(orbiter)

    def adjacents(self, space_object):
        return self.adjency_list[space_object]

class OrbitTransferGraph:
    """
    Undirected graph describing the object's orbit
    Allowing to move for one object to another whatever
    the direction
    """
    def __init__(self, orbit_description_file_path):
        self.adjency_list = defaultdict(list)
        with open(orbit_description_file_path) as f:
            for l in f:
                center, orbiter = l.rstrip('\n').split(')')
                self.adjency_list[center].append(orbiter)
                self.adjency_list[orbiter].append(center)

    def adjacents(self, space_object):
        return self.adjency_list[space_object]

class DirectAndIndirectPaths:
    def __init__(self, orbit_graph):
        self.orbit_graph = orbit_graph
        self.nb_directs = 0
        self.nb_indirects = 0
        # source vertex is 'COM'
        self.count_paths('COM')

    def count_paths(self, space_object):
        adjs = self.orbit_graph.adjacents(space_object)

        # increment the number of direct orbit
        # by the number of adjacents of current vertex
        nb_adjs = len(adjs)
        self.nb_directs += nb_adjs

        # count the number indirects orbits by 
        # the number of orbits of the adjacents
        nb_direct_adjacents = 0
        for orbiter in adjs:
            nb_direct_adjacents += self.count_paths(orbiter)
        self.nb_indirects += nb_direct_adjacents

        # return the number of orbits (direct + indirect)
        # to the parent object
        return nb_adjs + nb_direct_adjacents

class BFS:
    """
    Breadth first search implementation
    to search shortest path
    """
    def __init__(self, orbital_transfer_graph, source, destination):
        self.orbital_transfer_graph = orbital_transfer_graph
        self.marked = {}
        self.path_len = None

        vertices_to_visit = []
        vertices_to_visit.append((source, 0))
        while vertices_to_visit:
            vertex, level = vertices_to_visit.pop(0)
            if self.is_marked(vertex):
                continue
            if vertex == destination:
                # vertex YOU/SAN don't count
                self.path_len = level - 2
                return
            self.mark(vertex)
            for v in self.orbital_transfer_graph.adjacents(vertex):
                vertices_to_visit.append((v, level+1))

    def mark(self, vertex):
        self.marked[vertex] = True

    def is_marked(self, vertex):
        return self.marked.get(vertex, False)

if __name__ == '__main__':
    og = OrbitGraph('/mnt/c/Users/Bertrand/Documents/advent/input4_com_orbits_day6.txt')
    path_counter = DirectAndIndirectPaths(og)
    print(f'directs:{path_counter.nb_directs}/indirects:{path_counter.nb_indirects}/Sum:{path_counter.nb_directs+path_counter.nb_indirects}')

    otg = OrbitTransferGraph('/mnt/c/Users/Bertrand/Documents/advent/input4_com_orbits_day6.txt')
    bfs = BFS(otg, 'YOU', 'SAN')
    print(f'path len {bfs.path_len}')
