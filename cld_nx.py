import networkx as nx
import itertools as it
import matplotlib.pyplot as plt
def draw_labeled_multigraph(G, attr_name, mapping, ax=None):

    """
    Draws a labeled multigraph using NetworkX and Matplotlib.
    https://networkx.org/documentation/stable/auto_examples/drawing/plot_multigraphs.html
    """
    # Works with arc3 and angle3 connectionstyles
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    # connectionstyle = [f"angle3,angleA={r}" for r in it.accumulate([30] * 4)]
    G = nx.relabel_nodes(G, mapping, copy=False)

    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="blue", node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
    nx.draw_networkx_edges(
        G, pos, edge_color="red", connectionstyle=connectionstyle, ax=ax
    )

    labels = {
        tuple(edge): f"{attr_name}={attrs[attr_name]}"
        for *edge, attrs in G.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        G,
        pos,
        labels,
        connectionstyle=connectionstyle,
        label_pos=0.3,
        font_color="red",
        bbox={"alpha": 0},
        ax=ax,
    )
    plt.tight_layout()
    # plt.show()

