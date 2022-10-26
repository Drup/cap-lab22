""" Python Classes for Oriented and Non Oriented Graphs
"""

from graphviz import Digraph  # for dot output
from typing import List, Dict, Set, Tuple, Any


class GraphError(Exception):
    """Exception raised for self loops.
    """

    message: str

    def __init__(self, message: str):
        self.message = message


class GeneralGraph(object):
    """
    General class regrouping similarities
    between directed and non oriented graphs.
    The only differences between the two are:

    - how to compute the set of edges
    - how to add an edge
    - how to print the graph
    - how to delete a vertex
    - how to delete an edge
    - we only color undirected graphs
    """

    graph_dict: Dict[Any, Set]

    def __init__(self, graph_dict=None):
        """
        Initializes a graph object.
        If no dictionary or None is given,
        an empty dictionary will be used.
        """
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def vertices(self) -> List[Any]:
        """Return the vertices of a graph."""
        return list(self.graph_dict.keys())

    def add_vertex(self, vertex: Any) -> None:
        """
        If the vertex "vertex" is not in
        self.graph_dict, a key "vertex" with an empty
        list as a value is added to the dictionary.
        Otherwise nothing has to be done.
        """
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = set()

    def edges(self) -> List[Set]:
        """Return the edges of the graph."""
        return []

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.edges():
            res += str(edge) + " "
        return res

    def dfs_traversal(self, root: Any) -> List[Any]:
        """
        Compute a depth first search of the graph,
        from the vertex root.
        """
        seen: List[Any] = []
        todo: List[Any] = [root]
        while len(todo) > 0:  # while todo ...
            current = todo.pop()
            seen.append(current)
            for neighbour in self.graph_dict[current]:
                if neighbour not in seen:
                    todo.append(neighbour)
        return seen

    def is_reachable_from(self, v1: Any, v2: Any) -> bool:
        """True if there is a path from v1 to v2."""
        return v2 in self.dfs_traversal(v1)

    def connected_components(self) -> List[List[Any]]:
        """
        Compute the list of all connected components of the graph,
        each component being a list of vetices.
        """
        components: List[List[Any]] = []
        done: List[Any] = []
        for v in self.vertices():
            if v not in done:
                v_comp = self.dfs_traversal(v)
                components.append(v_comp)
                done.extend(v_comp)
        return components

    def bfs_traversal(self, root: Any) -> List[Any]:
        """
        Compute a breadth first search of the graph,
        from the vertex root.
        """
        seen: List[Any] = []
        todo: List[Any] = [root]
        while len(todo) > 0:  # while todo ...
            current = todo.pop(0)  # list.pop(0): for dequeuing (on the left...) !
            seen.append(current)
            for neighbour in self.graph_dict[current]:
                if neighbour not in seen:
                    todo.append(neighbour)
        return seen


class Graph(GeneralGraph):
    """Class for non oriented graphs."""

    def edges(self) -> List[Set]:
        """
        A static method generating the set of edges
        (they appear twice in the dictionnary).
        Return a list of sets.
        """
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def add_edge(self, edge: Tuple[Any, Any]) -> None:
        """
        Add an edge in the graph.
        edge should be a pair and not (c,c)
        (we call g.add_edge((v1,v2)))
        """
        (vertex1, vertex2) = edge
        if vertex1 == vertex2:
            raise GraphError("Cannot add a self loop on vertex {} in an unoriented graph.".format(
                             str(vertex1)))
        if vertex1 in self.graph_dict:
            self.graph_dict[vertex1].add(vertex2)
        else:
            self.graph_dict[vertex1] = {vertex2}
        if vertex2 in self.graph_dict:
            self.graph_dict[vertex2].add(vertex1)
        else:
            self.graph_dict[vertex2] = {vertex1}

    def print_dot(self, name: str, colors={}) -> None:
        """Print the graph."""
        color_names = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta'] + \
            [f"grey{i}" for i in range(0, 100, 10)]
        color_shapes = ['ellipse', 'box', 'diamond', 'trapezium', 'egg',
                        'parallelogram', 'house', 'triangle', 'pentagon', 'hexagon',
                        'septagon', 'octagon']
        dot = Digraph(comment='Conflict Graph')
        for k in self.graph_dict:
            shape = None
            if not colors:
                color = "red"  # Graph not colored: red for everyone
            elif k not in colors:
                color = "grey"  # Node not colored: grey
            else:
                n = colors[k]
                if n < len(color_names):
                    color = color_names[colors[k]]
                else:
                    color = "black"  # Too many colors anyway, it won't be readable.
                shape = color_shapes[n % len(color_shapes)]
            dot.node(str(k), color=color, shape=shape)
        for (v1, v2) in self.edges():
            dot.edge(str(v1), str(v2), dir="none")
        # print(dot.source)
        dot.render(name, view=True)  # print in pdf

    def delete_vertex(self, vertex: Any) -> None:
        """Delete a vertex and all the adjacent edges."""
        gdict = self.graph_dict
        for neighbour in gdict[vertex]:
            gdict[neighbour].remove(vertex)
        del gdict[vertex]

    def delete_edge(self, edge: Tuple[Any, Any]):
        """Delete an edge."""
        (v1, v2) = edge
        self.graph_dict[v1].remove(v2)
        self.graph_dict[v2].remove(v1)

    def color(self) -> Dict[Any, int]:
        """
        Color the graph with an unlimited number of colors.
        Return a dict vertex -> color, where color is an integer (0, 1, ...).
        """
        coloring, _, _ = self.color_with_k_colors()
        return coloring

    # see algo of the course
    def color_with_k_colors(self, K=None, avoidingnodes=()) -> Tuple[Dict[Any, int], bool, List]:
        """
        Color with <= K colors (if K is unspecified, use unlimited colors).

        Return 3 values:

        - a dict vertex -> color
        - a Boolean, True if the coloring succeeded
        - the set of nodes actually colored

        Do not color vertices belonging to avoidingnodes.

        Continue even if the algo fails.
        """
        if K is None:
            K = len(self.graph_dict)
        todo_vertices = []
        is_total = True
        gcopy = Graph(self.graph_dict.copy())
        # suppress nodes that are not to be considered.
        for node in avoidingnodes:
            gcopy.delete_vertex(node)
        # append nodes in the list according to their degree and node number:
        while gcopy.graph_dict:
            todo = list(gcopy.graph_dict)
            todo.sort(key=lambda v: (len(gcopy.graph_dict[v]), str(v)))
            lower = todo[0]
            todo_vertices.append(lower)
            gcopy.delete_vertex(lower)
        # Now reverse the list: first elements are those with higher degree
        # print(todo_vertices)
        todo_vertices.reverse()  # in place reversal
        # print(todo_vertices)
        coloring = {}
        colored_nodes = []
        # gdict will be the coloring map to return
        gdict = self.graph_dict
        for v in todo_vertices:
            seen_neighbours = [x for x in gdict[v] if x in coloring]
            choose_among = [i for i in range(K) if not (
                i in [coloring[v1] for v1 in seen_neighbours])]
            if choose_among:
                # if the node can be colored, I choose the minimal color.
                color = min(choose_among)
                coloring[v] = color
                colored_nodes.append(v)
            else:
                # if I cannot color some node, the coloring is not Total
                # but I continue
                is_total = False
        return (coloring, is_total, colored_nodes)


class DiGraph(GeneralGraph):
    """Class for directed graphs."""

    def pred(self, v: Any) -> Set:
        """Return all predecessors of the vertex `v` in the graph."""
        return {src for src, dests in self.graph_dict.items() if v in dests}

    def neighbourhoods(self) -> List[Tuple[Any, Set]]:
        """Return all neighbourhoods in the graph."""
        return list(self.graph_dict.items())

    def edges(self) -> List[Tuple[Any, Any]]:
        """ A static method generating the set of edges"""
        edges = []
        for vertex in self.graph_dict:
            for neighbour in self.graph_dict[vertex]:
                edges.append((vertex, neighbour))
        return edges

    def add_edge(self, edge: Tuple[Any, Any]) -> None:
        """
        Add an edge in the graph.
        edge should be a pair and not (c,c)
        (we call g.add_edge((v1,v2)))
        """
        (vertex1, vertex2) = edge
        if vertex1 in self.graph_dict:
            self.graph_dict[vertex1].add(vertex2)
        else:
            self.graph_dict[vertex1] = {vertex2}
        if vertex2 not in self.graph_dict:
            self.graph_dict[vertex2] = set()

    def print_dot(self, name: str) -> None:
        """Print the graph."""
        dot = Digraph(comment='Conflict Graph')
        for k in self.graph_dict:
            shape = None
            color = "grey"
            dot.node(str(k), color=color, shape=shape)
        for (v1, v2) in self.edges():
            dot.edge(str(v1), str(v2), dir="none")
        # print(dot.source)
        dot.render(name, view=True)  # print in pdf

    def delete_vertex(self, vertex: Any) -> None:
        """Delete a vertex and all the adjacent edges."""
        for node, neighbours in self.graph_dict.items():
            if vertex in neighbours:
                neighbours.remove(vertex)
        del self.graph_dict[vertex]

    def delete_edge(self, edge: Tuple[Any, Any]) -> None:
        """Delete an edge."""
        (v1, v2) = edge
        self.graph_dict[v1].remove(v2)
