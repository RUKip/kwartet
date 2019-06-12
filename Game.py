import time
from copy import deepcopy
import logging
import random

from ComputerAgent import ComputerAgent
from Card import Card
from Model import Model
import GraphPrinting


class Game(object):

    agents = {}         #{agent_id => Agent}
    cards_in_play = {}  #{agent_id => {group => [Cards]}}
    scores = {}         #{agent_id => score}

    def __init__(self, has_human_player):
        self.hasHuman = has_human_player

    def initGame(self, player_cnt):
        # create initial model
        model = Model(player_cnt)
        model.initModel()

        # create agents and set model
        for x in range(1, player_cnt+1):
            opponents = list(range(1, player_cnt+1))
            opponents.remove(x)
            agent = ComputerAgent(x, opponents)
            agent.setModel(deepcopy(model))
            self.agents[x] = agent
            self.cards_in_play[agent.id] = {}

        #if self.hasHuman:
            #self.agents[player_cnt] = HumanAgent()

        # divide cards randomly over agents
        all_groups = model.group_model.keys()
        all_cards = []
        for group in all_groups:
            for card in model.card_model[group][1].keys():
                all_cards.append((group,card))
                for agent_id in self.agents:
                    self.cards_in_play[agent_id][group] = []

        while(len(all_cards)>=1):
            for agent_id in self.agents:
                # might happen if not every agent gets the same amount of cards
                if len(all_cards)<1:
                    break
                (group, name) = random.choice(all_cards)
                all_cards.remove((group,name))
                random_card = Card(group, name)
                self.cards_in_play[agent_id][group].append(random_card)
                
        # Initialize agent specific models
        for agent in self.agents.values():
            agent_card_set = deepcopy(self.cards_in_play[agent.id])
            agent.generateInitialModel(agent_card_set)

        # I have to do the loop here bc the opponent models are not initialized
        # in the previous loop iterations
        for agent in self.agents.values():
            kwartet_group = agent.checkKwartet()
            if len(kwartet_group) > 0:
                for group in kwartet_group:
                    agent.remove_group(group)
                    self.cards_in_play[agent.id][group].clear()
                    agent.score += 1
                    for opponent in agent.opponents:
                        self.agents[opponent].AnnouncementKwartet(group)

            logging.debug("Opponents for agent " + str(agent.id) + ": " + str(agent.opponents))
            logging.info("Card model for agent " + str(agent.id) + ": " + str(agent.model.card_model))

        logging.info("Players card division is: " + str(self.cards_in_play))

        for a in self.agents.values():
            filename = "Initial-model"
            GraphPrinting.create_graph(a, filename)


    def startGame(self):
        #play untill no more agents are in the game
        agent = random.choice(list(self.agents.values()))
        logging.info("Player " + str(agent.id) + " is going to start the game")
        round = 0
        while(agent):
            round += 1
            logging.info("-------- Starting round {} --------".format(round))

            self.print_agent_graphs(round)
            agent = self.askingRound(agent)

            #Do some reasoning (all agents)
            for a in self.agents.values():
                a.basic_thinking()

            self.applyReasoningStrategies()

        logging.info("scores: " + str(self.scores))
        return self.scores

    def askingRound(self, current_player):
        logging.info("Starting a question round for player " + str(current_player.id) + ": ")
        (card, player_id) = current_player.makeDecision()
        logging.debug("Card choice: " + str(card) + ", to player: " + str(player_id))
        if (card is None):  # no more card options
            self.agents.pop(current_player.id)
            for a in self.agents.values():
                a.opponents.remove(current_player.id)
            self.scores[current_player.id] = current_player.getScore()
            logging.info("FATALITY!! Player " + str(current_player.id) + " has no more options, picking random new player")
            if not self.agents.values():
                logging.info("\n--------------------------------\nGame over!")
                return False
            self.outOfGame(current_player.id)
            return random.choice(list(self.agents.values()))
        else:
            logging.info("Player " + str(current_player.id) + " asked player " + str(player_id) + " for card " + str(
                card.getGroup()) + ":" + str(card.getCard()))
            asked_player = self.agents[player_id]
            if card in self.cards_in_play[player_id][card.getGroup()]:
                logging.info("Player " + str(player_id) +
                             " gave player " + str(current_player.id) +
                             " the card " + str(card.getCard()))
                for player in self.agents.values():
                    player.AnnouncementGaveCard(card, current_player.id, asked_player.id)
                self.transferCard(card, asked_player, current_player)
                return current_player
            else:
                logging.info("Player " + str(player_id) + " does not have the card " + str(card.getCard()))
                for player in self.agents.values():
                    player.AnnouncementNotCard(card, current_player.id, asked_player.id)
                return asked_player

    def transferCard(self, card, from_player, to_player):
        from_player.removeCard(card)
        to_player.giveCard(card)
        self.cards_in_play[from_player.id][card.getGroup()].remove(card)
        self.cards_in_play[to_player.id][card.getGroup()].append(card)
        if self.hasEmptyHand(from_player.id):
            logging.info("Another death claimed by kwartet, Player " + str(from_player.id) + " is out of cards")
            self.outOfGame(from_player.id)

        kwartet_group = to_player.checkKwartet()
        if len(kwartet_group) > 0:
            for group in kwartet_group:
                to_player.remove_group(group)
                self.cards_in_play[to_player.id][group].clear()
                to_player.score += 1
                for opponent in to_player.opponents:
                    self.agents[opponent].AnnouncementKwartet(group)

    def hasEmptyHand(self, player_id):
        for group in self.cards_in_play[player_id]:
            if(self.cards_in_play[player_id][group]):
               return False
        return True

    def outOfGame(self, player_id):
        for agent in self.agents.values():
            agent.sorrowPlayer(player_id)


    def print_agent_graphs(self, round):
        # Let's print some graphs..
        filename = "round-" + str(round)
        for a in self.agents.values():
            GraphPrinting.create_graph(a, filename)

    def applyReasoningStrategies(self):
        if 1 in self.agents:  # If we have a player 1, it is an advanced player:
            self.agents[1].advanced_thinking()