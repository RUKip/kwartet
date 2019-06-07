from graphviz import Graph

from Model import Model


def create_graph(agent, filename):
    color_mapping = {Model.WORLD_KNOWN: 'green', Model.WORLD_MAYBE: 'lightsalmon3', Model.WORLD_DELETED: 'red4'}
    filename = "output-graphs/borrar.png"
    card_model = agent.model.card_model
    group_model = agent.model.group_model

    # g = Graph('G', filename='process.gv', engine='sfdp', format='x11')
    g = Graph(name='knowledge_model', filename='knowledge_model.gv', format='x11')
    g.attr(compound='true', rankdir='TB')
    # g.attr(compound='true')

    with g.subgraph(name='group-player') as s:
        for group in group_model.keys():
            s.edge("Player " + str(agent.id) + " model", group)
            for player in card_model[group].keys():
                g.node(group + "-Player " + str(player), label="Player " + str(player))
                g.edge(group, group + "-Player " + str(player))

    with g.subgraph(name='player-card') as s:
        for group in group_model.keys():
            for player in card_model[group].keys():
                for card in card_model[group][player].keys():
                    node_name = str(player) + "-" + card
                    color = color_mapping[card_model[group][player][card]]
                    g.attr('node', style='filled', fillcolor=color)
                    g.node(node_name, label=card)

    # Create connections between subgraphs
    for group in group_model.keys():
        for player in card_model[group].keys():
            for card in card_model[group][player].keys():
                g.edge(group + "-Player " + str(player), str(player) + "-" + card)
    g.view(quiet=True)

    # g.render('test-output/round-table.gv', view=True)
    # g.render(view=True)

    # time.sleep(1)
    # g.attr('node', color='red', style='filled')

    print("Bye")
