import time

from Agent import Agent
from Card import Card
from Model import Model
import random

class Game(object):

    agents = []
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
            agent = Agent(x)
            agent.setModel(model)
            self.agents.append(agent)
            self.cards_in_play[agent.id] = []

        # divide cards randomly over agents
        all_groups = model.group_model.keys()
        all_cards = []
        for group in all_groups:
            for card in model.card_model[group][1].keys():
                all_cards.append((group,card))

        while(len(all_cards)>1):
            for agent in self.agents:
                (group, name) = random.choice(all_cards)
                all_cards.remove((group,name))
                random_card = Card(group, name)
                self.cards_in_play[agent.id].append(random_card)
                agent.giveCard(random_card, agent.id)

        #intialize agent specific models
        for agent in self.agents:
            agent.generateInitialModel(self.cards_in_play[agent.id])

        print("Agent card division is: " + str(self.cards_in_play)) #log this

    def startGame(self):
        #play untill no more agents are in the game
        while(self.agents):
            for player in self.agents:
                (card, player_id) = player.makeDecision()
                if(card is None):   #no more card options
                    self.agents.remove(player)
                    self.scores[player.id] = player.getScore()
                    print("FATALITY!!")
                else:
                    print("Agent " + str(player.id) + ", asked player " + player_id + " for card " + card.getGroup() + ":" + card.getCard())
                time.sleep(2) #wait 2 seconds for before making another decision

        #TODO: count score here
