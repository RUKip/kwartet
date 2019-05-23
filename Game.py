from Agent import Agent
from Model import Model
import random

class Game(object):

    agents = []
    cards_in_play = {}

    def initGame(self):
        player_cnt = None
        while player_cnt is None:
            try:
                player_cnt = int(input("How many players?: "))
                if(player_cnt<1):
                    raise Exception("Too small player count!")
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
                all_cards.append((group, card))

        while(len(all_cards)>1):
            for agent in self.agents:
                random_card = random.choice(all_cards)
                all_cards.remove(random_card)
                self.cards_in_play[agent.id].append(random_card)
                agent.giveCard(random_card)

        print("Agent card division is: " + str(self.cards_in_play)) #log this

    def startGame(self):
        return None
        #do some game loop here
