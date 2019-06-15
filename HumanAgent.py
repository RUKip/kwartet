import logging
import time

from Agent import Agent
import InputHandler
from Card import Card


class HumanAgent(Agent):

    REFLECTION_TIME = 5

    def makeDecision(self):
        logging.info("Human player's turn")
        print("It is your turn!")
        self.showCardSet()

        while True:
            agent_id = InputHandler.handleInput("Asking which player?: ", type_cast=int, human_agent=self)
            if (agent_id == self.id):
                print("Try not asking yourself")
            elif(not (agent_id in self.opponents)):
                print("Available agents are: " + str(self.opponents))
            else:
                break

        while True:
            card_name = InputHandler.handleInput("Which card? (syntax => group:card_name): ", human_agent=self)
            if not (self.is_valid(card_name)):
                print("That is not a card you can ask")
            else:
                break
        card_values = card_name.split(":")
        card = Card(card_values[0], card_name)
        return (card, agent_id)

    def generateInitialModel(self, init_card_set):
        self.card_set = init_card_set

    def sorrowPlayer(self, dead_player_id):
        print("deadplayerid: " + str(dead_player_id))    # debug
        print("own id: " + str(self.id)) #debug
        if dead_player_id == self.id:
            print("Seems your out of cards partner.. lets wait for the result")
        else:
            print("Player " + str(dead_player_id) + " sleeps with the fishes")
            print(self.opponents)

    def is_valid(self, card_name):
        print("checking if card: " + card_name + ", is valid")
        options = self.getOptions()
        if card_name in [str(option) for option in options]:
            return True
        return False

    def showCardSet(self):
        print(InputHandler.RESPONSE_BORDER)
        print("Cards in hand:")
        print(self.card_set)
        print(InputHandler.RESPONSE_BORDER)

    def getOptions(self):
        options = []
        for card in self.all_cards:
            card = Card(card[0], card[1])
            if card.getGroup() in self.card_set.keys():
                if not (card in self.card_set[card.getGroup()]):
                    options.append(card)
        return options

    def showAskOptions(self):
        options = self.getOptions()
        print(InputHandler.RESPONSE_BORDER)
        print("Possible options are: " + str(options))
        print(InputHandler.RESPONSE_BORDER)

    def AnnouncementGaveCard(self, card, asker_id, asked_id):
        if asked_id == self.id:
            print("Shame you gave " + str(card) + " to player " + str(asker_id))
        elif asker_id == self.id:
            print("Nice you got " + str(card) + " from player " + str(asked_id))
        else:
            print("Heads up, player " + str(asked_id) + " gave " + str(card) + " to player " + str(asker_id))

    def AnnouncementNotCard(self, card, asker_id, asked_id):
        if asked_id == self.id:
            print("You did not have " + str(card) + " for player " + str(asker_id))
        elif asker_id == self.id:
            print("Hmm que misterio, " + str(card) + " was not in possesion of player " + str(asked_id))
        else:
            print("Heads up, player " + str(asked_id) + " could not give " + str(card) + " to player " + str(asker_id))

    def AnnouncementKwartet(self, group):
        print("k..k..k..Kwwaaartet!  group " + str(group) + " is now gone from the game")

    def basic_thinking(self):
        print("Your time to reflect and think about the big questions in life...")
        time.sleep(self.REFLECTION_TIME)

    def isHuman(self):
        return True