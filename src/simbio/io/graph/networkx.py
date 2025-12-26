from typing import assert_never

from networkx import DiGraph, Graph, bipartite

from ...core import Compartment, RateLaw, Species


def graph(model: type[Compartment], /) -> DiGraph:
    """Construct a directed bipartite graph of Species and Reactions."""
    g = DiGraph()
    for x in model._yield(Species | RateLaw):  # type: ignore
        match x:
            case Species():
                g.add_node(x)
            case RateLaw():
                name = str(x)
                g.add_node(name, reaction=x)
                for r in x.reactants:
                    g.add_edge(r.variable, name, stoichiometry=r.stoichiometry)
                for p in x.products:
                    g.add_edge(name, p.variable, stoichiometry=p.stoichiometry)
            case _:
                assert_never(x)
    return g


def to_species_graph(graph: DiGraph, /) -> Graph:
    """Project a bipartite graph into the Species graph.

    Two Species are connected if they take part in the same Reaction.
    """
    return bipartite.projected_graph(
        graph,
        nodes=[n for n in graph if isinstance(n, Species)],
    )


def to_reaction_graph(graph: DiGraph, /) -> Graph:
    """Project a bipartite graph into the Reaction graph.

    Two Reactions are connected if they share a common Species.
    """
    return bipartite.projected_graph(
        graph,
        nodes=[n for n in graph if not isinstance(n, Species)],
    )
