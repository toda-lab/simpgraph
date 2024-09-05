simpgraph: Minimal Python Module for Unordered Graphs
================================================================

Introduction
============
``simpgraph`` is a simple and minimal Python module for unordered graphs.
An *unordered graph*, simply called a *graph*, is a pair of a set of elements, called *vertices*, 
and a set of (unordered) vertex pairs, called *edges*.
In this module, a graph is assumed to have no *loop*, an edge whose vertices
are identical with each other, and all edges have no direction.

Installation
============

.. code:: shell-session

    $ pip install simpgraph

Usage
=====

Let us import ``simpgraph`` module, create an empty graph, 
and add edges (and vertices if necessary).

.. code:: python

    from simpgraph import SimpGraph

    # empty graph
    g = SimpGraph()

    #   1
    #   |   
    #   4---3
    g.add_edge(4,1)
    g.add_edge(4,3)

    assert set(g.all_vertices()) == {1,3,4}
    assert g.num_vertices() == 3
    assert g.max_vertex()   == 4 # not always equal to the number of vertices

    assert set(g.adj_vertices(1)) == {4}
    assert set(g.adj_vertices(3)) == {4}
    assert set(g.adj_vertices(4)) == {1,3}

    assert g.num_edges() == 2
    g.add_edge(1,4) # the edge between 1 and 4 already added and nothing done
    assert g.num_edges() == 2

As above, ``add_edge(u,v)`` adds, to the edge set, 
the edge between vertices ``u,v`` given in its arguments in an arbitrary order.
New vertices, if included in the added edge, are also added to the vertex set.
If the edge is present in the edge set, the method does nothing.

.. code:: python

    #
    #   1   2
    #   |   
    #   4---3
    g.add_vertex(2)

    assert set(g.all_vertices()) == {1,2,3,4}
    assert set(g.all_edges())    == {(1,4),(3,4)}

    assert set(g.adj_vertices(2)) == set() # isolated vertex

    assert g.num_vertices() == 4
    g.add_vertex(1) # vertex 1 already present and nothing done
    assert g.num_vertices() == 4

Similary, ``add_vertex(u)`` adds vertex ``u`` to the vertex set.
If it is present in the vertex set, nothing is done.

.. code:: python

    #   before      after    
    #   1   2       1    2
    #   |       =>  |
    #   4---3       4    
    g.discard_vertex(3)
    
    assert set(g.all_vertices()) == {1,2,4}
    assert set(g.all_edges())    == {(1,4)}

    assert g.num_vertices() == 3
    g.discard_vertex(3) # vertex 3 already discarded and nothing done
    assert g.num_vertices() == 3

As above, ``discard_vertex(u)`` discards not only vertex ``u`` 
but also all edges incident to ``u``.
If the vertex is not present in the graph, nothing is done 
and no exception raises

.. code:: python

    #   before      after    
    #   1   2       1    2
    #   |       =>  
    #   4           4    
    g.discard_edge(1,4)

    assert set(g.all_vertices()) == {1,2,4}
    assert set(g.all_edges())    == set()

    assert g.num_edges() == 0
    g.discard_edge(1,4)
    assert g.num_edges() == 0

Similary, ``discard_edge(u,v)`` discards the edge between ``u`` and ``v``
If the edge is not present in the graph, nothing is done and no exception
raises.

.. code:: python

    #   before      after    
    #   1   2       
    #           =>  
    #   4               
    g.clear()

    assert g.num_vertices() == 0
    assert g.num_edges()    == 0

``clear()`` clears all variables of graph ``g`` and makes it an empty graph.

.. code:: python

    #   1    2:B
    #   |A   |
    #   4    3:C
    g.add_edge(2,3)
    g.add_edge(1,4, label="A")
    g.add_vertex(2, label="B")
    g.add_vertex(3, label="C")

    assert g.vertex_label(1) is None
    assert g.vertex_label(2) == "B"
    assert g.vertex_label(3) == "C"
    assert g.vertex_label(4) is None

    assert g.edge_label(2,3) is None
    assert g.edge_label(1,4) == "A"

    #   before       after
    #   1    2:B     1    2:B
    #   |A   |    => |A   |D
    #   4    3:C     4    3:C
    g.add_edge(2,3, label="D") # label updated

Optional labels can be assigned to vertices and edges,
and the graph can be rendered as follows.

.. code:: python

    g.render(filename="sample", format="png")

As a result, ``sample.png`` will be generated.
The arguments of ``render()`` are the same as those of ``render()`` of
Graphviz.
See `User Guide of Graphviz
<https://graphviz.readthedocs.io/en/stable/manual.html>`__ .

.. code:: python

    #   1    2:B
    #   |A   |D
    #   4    3:C
    g.add_edge(1,2, label="D")
    with open("sample.col", "w") as f:
        f.write(f"p {g.max_vertex()} {g.num_edges()}\n")
        for u in g.all_vertices():
            f.write(f"n {u}\n")
        for u,v in g.all_edges():
            f.write(f"e {u} {v}\n")
        f.seek(0)

    gg = SimpGraph.read(filename="sample.col", format="DIMACS")

    assert(g == gg) # the vertex set and the edge set are determined to be equal.

    # However, no label is preserved in the constructed graph.
    #   1    2
    #   |    |
    #   4    3
    assert gg.vertex_label(2) is None
    assert gg.vertex_label(3) is None
    assert gg.edge_label(1,4) is None
    assert gg.edge_label(2,3) is None

As above, a graph can be wrote to an external file in DIMACS graph format,
but vertex labels and edge labels are not recorded.
Class method ``SimpGraph.read()`` reads such a file and construct a graph,
and the resulted graph ``g`` is equal to the original graph ``g``
in that they have the same vertex set and the same edge set.
(Note: the vertex labels and the edge labels are not considered).

Bugs/Requests/Discussions
=========================

Please report bugs and requests from `GitHub Issues
<https://github.com/toda-lab/simpgraph/issues>`__ , and 
ask questions from `GitHub Discussions <https://github.com/toda-lab/simpgraph/discussions>`__ .

License
=======

Please see `LICENSE <https://github.com/toda-lab/simpgraph/blob/main/LICENSE>`__ .
