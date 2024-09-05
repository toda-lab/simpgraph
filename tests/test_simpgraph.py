import tempfile

from simpgraph import SimpGraph

def test_simpgraph():
    testcases = [\
        #  1---2 
        #  |
        #  3   4
        ((1,2,3,4), ((1,2),(1,3)), {1:{2,3}, 2:{1}, 3:{1}, 4:set()}),
        #  1   2
        #
        #  3   4
        ((1,2,3,4), (), {1:set(), 2:set(), 3:set(), 4:set()}),
    ]

    g = SimpGraph()
    for V,E,A in testcases:
        g.clear()
        for u in V:
            g.add_vertex(u)
        for u,v in E:
            g.add_edge(u,v)
        assert(set(g.all_vertices()) == set(V))
        assert(set(g.all_edges())    == set(E))
        assert(g.num_vertices() == len(V))
        assert(g.num_edges()    == len(E))
        assert(g.max_vertex()   == max(V))
        for u in g.all_vertices():
            assert(set(g.adj_vertices(u)) == A[u])


def test_add_discard():
    testcases = [
        (
            # Operations
            (
            #  1   2 
            #  |
            #  3   4
            ("add_edge", (3,1)),
            #  1   2 
            #  |
            #  3   4
            ("add_edge", (3,1)),
            #  1---2 
            #  |
            #  3   4
            ("add_edge", (1,2)),
            #  1---2 
            #  |
            #  3---4
            ("add_edge", (4,3)),
            #  1---2 
            #  
            #  3---4
            ("discard_edge", (1,3)),
            #  1---2 
            #  
            #  3---4
            ("discard_edge", (1,3)),
            #  1---2 
            #      |
            #  3---4
            ("add_edge", (4,2)),
            #  1   2 
            #      |
            #  3---4
            ("discard_edge", (1,2)),
            ),
            # Answers
            (
            {1,2,3,4}, # vertex set
            {(3,4), (2,4)}, # edge set
            {1:set(), 2:{4}, 3:{4}, 4:{2,3}} # adjacency
            )
        ),
        (
            # Operations
            (
            #  1
            #
            #
            ("add_vertex", (1,)),
            #  1
            #
            #  3
            ("add_vertex", (3,)),
            #  1
            #
            #  3    4
            ("add_vertex", (4,)),
            #  1
            #
            #  3----4
            ("add_edge", (4,3)),
            #  1
            #  |
            #  3----4
            ("add_edge", (1,3)),
            #  1
            #  
            #       4
            ("discard_vertex", (3,)),
            #  1
            #  
            #       4
            ("discard_vertex", (3,)),
            #       
            #       
            #       4
            ("discard_vertex", (1,)),
            #  1----2
            #       
            #       4
            ("add_edge", (2,1)),
            ),
            # Answers
            (
            {1,2,4},
            {(1,2)},
            {1:{2}, 2:{1}, 4:set()}
            )
        ),
    ]

    g = SimpGraph()
    for S, A in testcases:
        g.clear()
        for op, args in S:
            if op == "add_edge":
                g.add_edge(args[0],args[1])
            elif op == "discard_edge":
                g.discard_edge(args[0],args[1])
            elif op == "add_vertex":
                g.add_vertex(args[0])
            elif op == "discard_vertex":
                assert(len(args)==1)
                g.discard_vertex(args[0])
            else:
                raise Exception("Unknown operation")
        assert(A[0] == set(g.all_vertices()))
        assert(A[1] == set(g.all_edges()))
        for u in g.all_vertices():
            assert(set(g.adj_vertices(u)) == A[2][u])

def test_label():
    testcases = [
        (
            # Operations
            (
            # 1:A
            #
            #
            ("add_vertex", (1,), "A"),
            # 1:A
            #
            # 3:C
            ("add_vertex", (3,), "C"),
            # 1:A    2:?
            #         |
            # 3:C    4:?
            ("add_edge", (2,4), None),
            # 1:A ---2:?
            #     t  |
            # 3:C    4:?
            ("add_edge", (1,2), "t"),
            #        2:?
            #        |
            # 3:C    4:?
            ("discard_vertex", (1,), None),
            # 1:?    2:?
            #        |
            # 3:C    4:?
            ("add_vertex", (1,), None),
            # 1:?----2:?
            #        |
            # 3:C    4:?
            ("add_edge", (1,2), None),
            # 1:?----2:C
            #        | r
            # 3:C    4:?
            ("add_vertex", (2,), "C"),
            # 1:?----2:C
            #        | r
            # 3:C    4:?
            ("add_edge", (4,2), "r"),
            ),
            # Answers
            (
            {1,2,3,4}, # vertex set
            {(1,2),(2,4)}, # edge_set
            {1:{2}, 2:{1,4}, 3:set(), 4:{2}}, # adjacency
            {2:"C", 3:"C"}, # vertex_label_dict
            {(2,4):"r"}, # edge_label_dict
            )
        ),
    ]

    g = SimpGraph()
    for S, A in testcases:
        g.clear()
        for op, args, label in S:
            if op == "add_edge":
                g.add_edge(args[0],args[1],label=label)
            elif op == "discard_edge":
                g.discard_edge(args[0],args[1])
            elif op == "add_vertex":
                g.add_vertex(args[0],label=label)
            elif op == "discard_vertex":
                assert(len(args)==1)
                g.discard_vertex(args[0])
            else:
                raise Exception("Unknown operation")
        assert(A[0] == set(g.all_vertices()))
        assert(A[1] == set(g.all_edges()))
        for u in g.all_vertices():
            assert(set(g.adj_vertices(u)) == A[2][u])
        for u in g.all_vertices():
            if g.vertex_label(u) is not None:
                assert(g.vertex_label(u) == A[3][u])
        for u in A[3]:
            assert(g.vertex_label(u) == A[3][u])
        for u,v in g.all_edges():
            if g.edge_label(u,v) is not None:
                assert(g.edge_label(u,v) == A[4][(u,v)])
        for u,v in A[4]:
            assert(g.edge_label(u,v) == A[4][(u,v)])

def test_read():
    testcases = [
        (
        # 1--2
        #
        # 3--4
        (1,2,3,4),    # V: vertices
        ((1,2),(3,4)) # E: edges
        ),
        (
        # 1  
        #
        # 3  4
        (1,3,4),
        ()
        ),
    ]

    g = SimpGraph()
    for V,E in testcases:
        g.clear()
        for u in V:
            g.add_vertex(u)
        for e in E:
            g.add_edge(e[0],e[1])
        with tempfile.NamedTemporaryFile("w") as f:
            f.write(f"p {g.max_vertex()} {g.num_edges()}\n")
            for u in g.all_vertices():
                f.write(f"n {u}\n")
            for e in g.all_edges():
                f.write(f"e {e[0]} {e[1]}\n")
            f.seek(0)
            gg = SimpGraph.read(filename=f.name, format="DIMACS")
            assert(g == gg)
