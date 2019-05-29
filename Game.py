import time
from copy import copy, deepcopy

from Agent import Agent
from Card import Card
from Model import Model
import random

class Game(object):

    agents = {}
    cards_in_play = {}
    scores = {}

    def initGame(self):
        player_cnt = None
        while player_cnt is None:
            try:
                player_cnt = int(input("How many players?: "))
                if(player_cnt<1):
                    print("Too small player count!")
                    player_cnt = None
            except:
                print("Not valid, try a different number")
                pass

        #create initial model
        model = Model(player_cnt)
        model.initModel()

        #create agents and set model
        for x in range(1, player_cnt+1):
            opponents = list(range(1, player_cnt+1))
            opponents.remove(x)
            agent = Agent(x, opponents)
            agent.setModel(deepcopy(model))
            self.agents[x] = agent
            self.cards_in_play[agent.id] = {}

        # divide cards randomly over agents
        all_groups = model.group_model.keys()
        all_cards = []
        for group in all_groups:
            for card in model.card_model[group][1].keys():
                all_cards.append((group,card))
                for agent_id in self.agents:
                    self.cards_in_play[agent_id][group] = []

        while(len(all_cards)>1):
            for agent_id in self.agents:
                (group, name) = random.choice(all_cards)
                all_cards.remove((group,name))
                random_card = Card(group, name)
                self.cards_in_play[agent_id][group].append(random_card)

        #intialize agent specific models
        for agent in self.agents.values():
            agent.generateInitialModel(deepcopy(self.cards_in_play[agent.id]))

        print("Agent card division is: " + str(self.cards_in_play)) #log this

    def startGame(self):
        #play untill no more agents are in the game
        agent = random.choice(list(self.agents.values()))
        print("Player " + str(agent.id) + " is going to start")
        while(agent):
            agent = self.askingRound(agent)
            time.sleep(2)  # wait 2 seconds for before making another decision
            print("\n-------------------------------------\n")

        #TODO: count score here
        print("scores: " + str(self.scores))


    def askingRound(self, current_player):
        if not self.agents.values():
            print("\n--------------------------------\nGame over!")
            return False

        print("Starting a question round for player " + str(current_player.id) + ": ")
        (card, player_id) = current_player.makeDecision()
        print('card choice: ' + str(card) + ", to player: " + str(player_id))
        if (card is None):  # no more card options
            self.agents.pop(current_player.id)
            self.scores[current_player.id] = current_player.getScore()
            print("FATALITY!!")
            print("Agent has no more options picking random new player")
            return random.choice(list(self.agents.values()))
        else:
            print("Agent " + str(current_player.id) + ", asked player " + str(player_id) + " for card " + str(
                card.getGroup()) + ":" + str(card.getCard()))
            asked_player = self.agents[player_id]
            if card in self.cards_in_play[player_id][card.getGroup()]:
                print("Agent " + str(current_player.id) + ", gave player " + str(player_id) + " the card " + str(card.getCard()))
                self.transferCard(card, asked_player,current_player)
                for player in self.agents.values():
                    player.AnnouncementGaveCard(card, current_player, asked_player)
                return current_player
            else:
                print("Agent " + str(current_player.id) + ", did not get the card " +  str(card.getCard() + " from player " + str(player_id)))
                for player in self.agents.values():
                    player.AnnouncementNotCard(card, current_player, asked_player)
                return asked_player

    def transferCard(self, card, from_player, to_player):
        to_player.giveCard(card)
        from_player.removeCard(card)
        self.cards_in_play[to_player.id][card.getGroup()].append(card)
        self.cards_in_play[from_player][card.getGroup()].remove(card)
