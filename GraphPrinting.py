from pathlib import Path

from graphviz import Graph

from Model import Model


def create_graph(agent, filename, on_line_view=False):
    if not agent.isHuman():
        color_mapping = {Model.WORLD_KNOWN: 'green', Model.WORLD_MAYBE: 'gray80', Model.WORLD_DELETED: 'gray10'}
        path = Path("knowledge-graphs") / ("Player-" + str(agent.id))
        if not path.is_dir():
            path.mkdir(parents=True)
        format = 'x11' if on_line_view else 'svg'
        card_model = agent.model.card_model
        group_model = agent.model.group_model

        g = Graph(name=filename, directory=path.as_posix(), format=format)
        g.attr(rankdir='LR')

        for group in group_model.keys():
            g.edge("Player " + str(agent.id) + " model", group)
            for player in card_model[group].keys():
                g.node(group + "-Player " + str(player), label="Player " + str(player))
                g.edge(group, group + "-Player " + str(player))

        for group in group_model.keys():
            for player in agent.model.players:
                for card in card_model[group][agent.id][player].keys():
                    node_name = str(player) + "-" + card
                    color = color_mapping[card_model[group][agent.id][player][card]]
                    g.attr('node', style='filled', fillcolor=color)
                    g.node(node_name, label=card)
                    g.edge(group + "-Player " + str(player), str(player) + "-" + card)

        view = True if on_line_view else False
        g.render(cleanup=True, view=view)
