import os
from typing import Set, Tuple, Union, Optional
from os import PathLike

import graphviz

class SimpGraph:
    """Simple and minimal implementation of unordered graph"""

    def __init__(self):
        """Creates an empty graph."""
        self._vertex_set = set()
        """Set of vertices"""
        self._edge_set   = set()
        """Set of edges"""
        self._adj_dict   = {}
        """Dictionary that maps each vertex to the set of adjacent vertices"""
        self._vertex_label_dict = {}
        """Dictionary that maps each vertex to its label"""
        self._edge_label_dict = {}
        """Dictionary that maps each edge to its label"""

    def clear(self) -> None:
        """Clears all object variables to make it an empty graph."""
        self._vertex_set.clear()
        self._edge_set.clear()
        self._adj_dict.clear()
        self._vertex_label_dict.clear()
        self._edge_label_dict.clear()

    def __eq__(self, g):
        """Determines equality as graphs without labels.

        Args:
            g: A graph

        Returns:
            True if the vertex set and the edge set are equal with each other.
        """
        return self._vertex_set == set(g.all_vertices())\
            and self._edge_set == set(g.all_edges())

    def add_vertex(self, u: int, label: Optional[str] = None) -> None:
        """Adds a vertex to the vertex set.

        Nothing is done if already added.

        Args:
            u: A vertex
            label: A vertex label
        
        Raises:
            TypeError: if u is not an int.
            ValueError: if u is not positive.
        """
        if type(u) is not int:
                raise TypeError()
        if u <= 0:
            raise ValueError("vertex index must be positive.")
        if u in self._vertex_set:
            if label is not None:
                self._vertex_label_dict[u] = label
            return
        assert(u not in self._adj_dict)
        self._adj_dict[u] = set()
        self._vertex_set.add(u)
        if label is not None:
            self._vertex_label_dict[u] = label

    def add_edge(self, u: int, v: int, label: Optional[str] = None) -> None:
        """Adds an edge to the edge set and updates adjacency relation.
        
        It is added as a sorted tuple to the edge set.
        A new vertex, if included in the edge, is added 
        with defaul label to the vertex set.
        Nothing is done if already added.

        Args:
            u: A vertex
            v: A vertex
            label: An edge label

        Raises:
            TypeError: if either u or v is not an int.
            ValueError: if either u or v is not positive.
            Exception: if u==v.
        """
        if type(u) is not int\
            or type(v) is not int:
                raise TypeError()
        if u <= 0 or v <= 0:
            raise ValueError("vertex index must be positive.")
        if u == v:
            raise Exception("cannot add loop.")
        if u > v:
            u,v = v,u
        if (u,v) in self._edge_set:
            if label is not None:
                self._edge_label_dict[(u,v)] = label
            return # already added
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj_dict[u].add(v)
        self._adj_dict[v].add(u)
        self._edge_set.add((u,v))
        if label is not None:
            self._edge_label_dict[(u,v)] = label
    
    def discard_vertex(self, u: int) -> None:
        """Removes a vertex if exists in the vertex set.
        
        The adjacency relation is updated so that 
        all edges incident to the vertex are also discarded.
        No exception raises if vertex does not exist.

        Args:
            u: A vertex
        """
        if u not in self._vertex_set:
            return # not present
        # NOTE: Do not use self._adj_dict[u] in the for statement
        # because self.discard_edge() changes self._adj_dict.
        neighbors = tuple(self._adj_dict[u])
        for v in neighbors:
            self.discard_edge(u,v)
        self._vertex_set.remove(u)
        self._vertex_label_dict.pop(u, None)
        self._adj_dict.pop(u)

    def discard_edge(self, u: int, v: int) -> None:
        """Removes an edge if exists in the edge set.
        
        No exception raises if edges does not exist.

        Args:
            u: A vertex
            v: A vertex
        """
        if u > v:
            u,v = v,u
        if (u,v) not in self._edge_set:
            return # not present
        self._edge_set.remove((u,v))
        self._edge_label_dict.pop((u,v), None)
        self._adj_dict[u].remove(v)
        self._adj_dict[v].remove(u)
    
    def num_vertices(self) -> int:
        """Gets the number of all vertices.
        
        Returns:
            The number of all vertices.
        """
        return len(self._vertex_set)

    def num_edges(self) -> int:
        """Gets the number of all edges.
        
        Returns:
            The number of all edges.
        """
        return len(self._edge_set)

    def max_vertex(self) -> int:
        """Gets the maximum index of a vertex.

        Returns:
            The maximum index of a vertex

        Note:
            max_vertex() not always equals to num_vertices()
            due to missing vertices.
        """
        return max(self._vertex_set)

    def all_vertices(self) -> Tuple[int]:
        """Gets the tuple of all vertices.

        Returns:
            The tuple of all vertices
        """
        return tuple(self._vertex_set)

    def all_edges(self) -> Tuple[Tuple[int]]:
        """Gets the tuple of all edges.

        Returns:
            The tuple of all edges
        """
        return tuple(self._edge_set)

    def adj_vertices(self, u: int) -> Tuple[int]:
        """Gets the tuple of adjacent vertices.
        
        Args:
            u: vertex index (> 0)

        Returns:
            The tuple of adjacent vertices.

        Raises:
            Exception: if u is an unknown vertex.
        """
        if u not in self._vertex_set:
            raise Exception(f"Unknown vertex: {u}")
        return tuple(self._adj_dict[u])

    def vertex_label(self, u: int) -> Optional[str]:
        """Gets the label of a vertex.
        
        Args:
            u: A vertex

        Returns:
            The label of vertex if exists, and None otherwise.

        Raises:
            Exception: if u is an unknown vertex.
        """
        if u not in self._vertex_set:
            raise Exception(f"Unknown vertex: {u}")
        if u in self._vertex_label_dict:
            return self._vertex_label_dict[u]
        else:
            return None

    def edge_label(self, u: int, v: int) -> Optional[str]:
        """Gets the label of an edge.
        
        Args:
            u: A vertex
            v: A vertex

        Returns:
            The label of edge if exists, and None otherwise.

        Raises:
            Exception: if u is an unknown vertex.
        """
        if u > v:
            u,v = v,u
        if (u,v) not in self._edge_set:
            raise Exception(f"Unknown edge: {u} {v}")
        if (u,v) in self._edge_label_dict:
            return self._edge_label_dict[(u,v)]
        else:
            return None

    @classmethod
    def read(cls, filename: Union[PathLike,str,None] = None,\
        format: Optional[str] = None) -> "SimpGraph":
        """Reads and constructs a graph from a file.

        Args:
            filename: A file name
            format: format of graph file ["DIMACS"]

        Returns:
            A graph object.

        Raises:
            Exception: if file does not exist.
            Exception: if unexpected format type is given.
            Exception: if unexpected format is found.
        """
        if not os.path.isfile(filename):
            raise Exception("Cannot find: "+filename)
        if format not in ["DIMACS"]:
            raise Exception("Unexpected format type")
        g = cls()
        with open(filename, "r") as f:
            if format == "DIMACS":
                for line in f.read().split("\n"):
                    res = line.strip().split(" ")
                    if len(res) > 0 and res[0] == "n":
                        if len(res) < 2:
                            raise Exception("Unexpected format: "+line)
                        g.add_vertex(int(res[1]))
                    if len(res) > 0 and res[0] == "e":
                        if len(res) < 3:
                            raise Exception("Unexpected format: "+line)
                        g.add_edge(int(res[1]),int(res[2]))
            else:
                raise Exception("Unexpected fomart type")
        return g


    def render(self, filename: Union[PathLike,str,None] = None,\
    directory: Union[PathLike,str,None] = None, view: bool = False,\
    cleanup: bool = False, format: Optional[str] = None,\
    renderer: Optional[str] = None, formatter: Optional[str] = None,\
    neato_no_op: Union[bool,int,None] = None, quiet: bool = False,\
    quiet_view: bool = False, outfile: Union[PathLike,str,None] = None,\
    engine: Optional[str] = None, raise_if_result_exists: bool = False,\
    overwrite_source: bool = False) -> None:
        """Saves the source to file and renders with the Graphviz engine.

        The arguments are the same as those of render() of Graphviz:
        https://graphviz.readthedocs.io/en/stable/manual.html .
        """
        dot = graphviz.Graph()
        for u in self._vertex_set:
            label = self.vertex_label(u)
            if label is None:
                label = str(u)
            dot.node(str(u), label=label)
        for e in self._edge_set:
            label_u = self.vertex_label(e[0])
            label_v = self.vertex_label(e[1])
            if label_u is None:
                label_u = str(e[0])
            if label_v is None:
                label_v = str(e[1])
            dot.edge(str(e[0]), str(e[1]), label=self.edge_label(e[0],e[1]))
        dot.render(filename=filename, directory=directory, view=view,\
            cleanup=cleanup, format=format, renderer=renderer,\
            formatter=formatter, neato_no_op=neato_no_op, quiet=quiet,\
            quiet_view=quiet_view, outfile=outfile, engine=engine,\
            raise_if_result_exists=raise_if_result_exists,\
            overwrite_source=overwrite_source)
