import pydot

from Model import Model


def create_graph(agent, filename):
    color_mapping = {Model.WORLD_KNOWN: 'green', Model.WORLD_MAYBE: 'orange', Model.WORLD_DELETED: 'red'}
    filename = filename + '.png'  # Just for now TODO: delete this
    card_model = agent.model.card_model
    group_model = agent.model.group_model
    groups = group_model.keys()
    n_groups = len(groups)

    graph = pydot.Dot(graph_type='graph')

    group = "farm_animals"
    # for player in card_model[group].keys():
    #     edge = pydot.Edge(group, "Player " + str(player))
    #     graph.add_edge(edge)

    card_nodes = []
    card_edges = []

    for player in card_model[group].keys():
        edge = pydot.Edge(group, "Player " + str(player))
        graph.add_edge(edge)
        for card in card_model[group][player].keys():
            node_name = str(player) + "_" + card
            color = color_mapping[card_model[group][player][card]]
            node = pydot.Node(node_name, style="filled", fillcolor=color)
            # card_nodes.append(node)
            graph.add_node(node)
            edge = pydot.Edge("Player " + str(player), node_name)
            graph.add_edge(edge)

    # for n in card_nodes:
    #     node, edge = n
    #     graph.add_node(node)
    #     graph.add_edge(edge)

    graph.write_png(filename)

    print("Bye")







    # for group in group_model.keys():
    #     for player in card_model[group].keys():
    #         edge = pydot.Edge(group, "Player " + str(player))
    #         graph.add_edge(edge)
    #         for card in card_model[group][player].keys():
    #             color = color_mapping[card_model[group][player][card]]
    #             graph.add_edge(pydot.Edge("Player " + str(player), card, color=color))
