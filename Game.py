import time
from copy import deepcopy
import logging
import random
from ComputerAgent import ComputerAgent
from HumanAgent import HumanAgent
from Card import Card
from Model import Model
import GraphPrinting

class Game(object):

    GAME_LOOP_TIME_SEC = 3 + HumanAgent.REFLECTION_TIME
    SEC_IN_MILLI = 100

    agents = {}         #{agent_id => Agent}
    cards_in_play = {}  #{agent_id => {group => [Cards]}}
    scores = {}         #{agent_id => score}

    def __init__(self, has_human_player):
        self.hasHuman = has_human_player

    def initGame(self, player_cnt):
        # create initial model
        model = Model(player_cnt)
        model.initModel()

        self.initAgents(player_cnt, model)

        all_cards = self.initCardsInPlay(model)
        self.divideCards(all_cards)

        # Initialize agent models
        for agent in self.agents.values():
            self.initAgentModel(agent, self.cards_in_play, all_cards)

            logging.debug("Opponents for agent " + str(agent.id) + ": " + str(agent.opponents))
            logging.info("Card model for agent " + str(agent.id) + ": " + str(agent.model.card_model))

        logging.info("Players card division is: " + str(self.cards_in_play))

        for a in self.agents.values():
            if not a.isHuman():
                filename = "Initial-model"
                GraphPrinting.create_graph(a, filename)


    # create agents and set model
    def initAgents(self, player_cnt, model):
        for x in range(1, player_cnt+1):
            opponents = list(range(1, player_cnt+1))
            opponents.remove(x)
            if (x == player_cnt) and self.hasHuman:
                agent = HumanAgent(player_cnt, list(range(1, player_cnt)))
            else:
                agent = ComputerAgent(x, opponents)
            agent.setModel(deepcopy(model))
            self.agents[x] = agent
            self.cards_in_play[agent.id] = {}


    #init and return initial set of cards
    def initCardsInPlay(self, model):
        all_groups = model.group_model.keys()
        all_cards = []
        for group in all_groups:
            for card in model.card_model[group][1][1].keys():
                all_cards.append((group,card))
                for agent_id in self.agents:
                    self.cards_in_play[agent_id][group] = []
        return all_cards

    def initAgentModel(self, agent, cards_in_play, all_cards):
        agent_card_set = deepcopy(cards_in_play[agent.id])
        agent.setAllCards(deepcopy(all_cards))
        agent.generateInitialModel(agent_card_set)

        kwartet_group = agent.checkKwartet()
        if len(kwartet_group) > 0:
            for group in kwartet_group:
                agent.remove_group(group)
                self.cards_in_play[agent.id][group].clear()
                agent.score += 1
                for opponent in agent.opponents:
                    self.agents[opponent].AnnouncementKwartet(group)

    # divide cards randomly over agents, until no cards left
    def divideCards(self, starting_cards):
        starting_cards_copy = deepcopy(starting_cards)
        while (len(starting_cards_copy) >= 1):
            for agent_id in self.agents:
                if len(starting_cards_copy) < 1:
                    break
                (group, name) = random.choice(starting_cards_copy)
                starting_cards_copy.remove((group, name))
                random_card = Card(group, name)
                self.cards_in_play[agent_id][group].append(random_card)


    def startGameLoop(self):
        #play untill no more agents are in the game
        agent = random.choice(list(self.agents.values()))
        logging.info("Player " + str(agent.id) + " is going to start the game")
        if self.hasHuman:
            print("-------------------------------------------------------")
            print("Player " + str(agent.id) + " is going to start the game")

        round = 0
        while(agent and self.agents):
            round += 1
            logging.info("-------- Starting round {} --------".format(round))
            if self.hasHuman:
                print("-------- Starting round {} --------".format(round))

            starting_time = time.time()
            agent = self.loopIteration(round,agent)
            elapsed_time = time.time() - starting_time

            if self.hasHuman:
                sleep_time = (self.GAME_LOOP_TIME_SEC - elapsed_time)
                if(sleep_time>0.0):
                    time.sleep(sleep_time)

        logging.info("scores: " + str(self.scores))
        return self.scores

    def loopIteration(self, round, agent):
        self.print_agent_graphs(round)
        new_agent = self.askingRound(agent)

        # Do some reasoning (all agents)
        for a in self.agents.values():
            a.basic_thinking()

        self.applyReasoningStrategies()
        return new_agent


    def askingRound(self, current_player):
        logging.info("Starting a question round for player " + str(current_player.id) + ": ")
        logging.info("scores: " + str(self.scores))
        (card, player_id) = current_player.makeDecision()
        logging.debug("Card choice: " + str(card) + ", to player: " + str(player_id))
        if (card is None):  # no more card options
            # ~ self.agents.pop(current_player.id)
            # ~ for a in self.agents.values():
                # ~ a.opponents.remove(current_player.id)
                # ~ a.model.players.remove(current_player.id)
            self.scores[current_player.id] = current_player.getScore()
            self.outOfGame(current_player.id)
            logging.info("FATALITY!! Player " + str(current_player.id) + " has no more options, picking random new player")
            if not self.agents.values():
                logging.info("\n--------------------------------\nGame over!")
                return False
            # ~ self.outOfGame(current_player.id)
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
            self.scores[from_player.id] = from_player.getScore()

        kwartet_group = to_player.checkKwartet()
        if len(kwartet_group) > 0:
            for group in kwartet_group:
                to_player.remove_group(group)
                self.cards_in_play[to_player.id][group].clear()
                to_player.score += 1
                for opponent in to_player.opponents:
                    self.agents[opponent].AnnouncementKwartet(group)
            if self.hasEmptyHand(to_player.id):
                logging.info("Player " + str(to_player.id) + " got no cards left")
                self.outOfGame(to_player.id)
                self.scores[to_player.id] = to_player.getScore()

    def hasEmptyHand(self, player_id):
        for group in self.cards_in_play[player_id]:
            if(self.cards_in_play[player_id][group]):
               return False
        return True

    def outOfGame(self, dead_player_id):
        if dead_player_id in self.agents:
            self.agents.pop(dead_player_id)
            for agent in self.agents.values():
                agent.sorrowPlayer(dead_player_id)

    def print_agent_graphs(self, round):
        # Let's print some graphs..
        filename = "round-" + str(round)
        for a in self.agents.values():
            GraphPrinting.create_graph(a, filename)

    def applyReasoningStrategies(self):
        if 1 in self.agents:  # If we have a player 1, it is an advanced player:
            self.agents[1].advanced_thinking()
