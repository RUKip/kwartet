import pydot
import cv2 as cv

from Model import Model


def create_graph(agent, filename):
    color_mapping = {Model.WORLD_KNOWN: 'green', Model.WORLD_MAYBE: 'lightsalmon3', Model.WORLD_DELETED: 'red4'}
    filename = "output-graphs/borrar.svg"
    # filename = filename + '.svg'  # Just for now TODO: delete this
    card_model = agent.model.card_model
    group_model = agent.model.group_model
    groups = group_model.keys()
    n_groups = len(groups)

    graph = pydot.Dot(graph_type='graph', rankdir='LR')


    # group = "farm_animals"

    for group in group_model.keys():
        graph.add_edge(pydot.Edge("Player " + str(agent.id) + " model", group))
        for player in card_model[group].keys():
            node_player = pydot.Node(group + "-Player " + str(player), label="Player " + str(player))
            edge = pydot.Edge(group, node_player)
            graph.add_edge(edge)
            for card in card_model[group][player].keys():
                node_name = str(player) + "-" + card
                color = color_mapping[card_model[group][player][card]]
                node = pydot.Node(node_name, style="filled", fillcolor=color, label=card)
                # card_nodes.append(node)
                graph.add_node(node)
                edge = pydot.Edge(node_player, node_name)
                graph.add_edge(edge)

    # for n in card_nodes:
    #     node, edge = n
    #     graph.add_node(node)
    #     graph.add_edge(edge)

    graph.write_svg(filename)


    print("Bye")







    # for group in group_model.keys():
    #     for player in card_model[group].keys():
    #         edge = pydot.Edge(group, "Player " + str(player))
    #         graph.add_edge(edge)
    #         for card in card_model[group][player].keys():
    #             color = color_mapping[card_model[group][player][card]]
    #             graph.add_edge(pydot.Edge("Player " + str(player), card, color=color))
