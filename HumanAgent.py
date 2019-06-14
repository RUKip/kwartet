import logging
import time

from copy import deepcopy, copy
from Agent import Agent
import InputHandler


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
            card = InputHandler.handleInput("Which card? (syntax => group:card_name): ", human_agent=self)
            group_cardname = card.split(":")
            if(not(len(group_cardname)==2)):
                print("Wrong syntax")
            elif(not self.is_valid(group_cardname[1])):
                print("That is not a card you can ask")
            else:
                break

    def generateInitialModel(self, init_card_set):
        self.card_set = init_card_set

    def sorrowPlayer(self, dead_player_id):
        if dead_player_id == self.id:
            print("Seems your out of cards partner.. lets wait for the result")
        else:
            print("Player " + str(dead_player_id) + " sleeps with the fishes")
            self.opponents.remove(dead_player_id)

    def is_valid(self, cardname):
        for card in self.all_cards:
            if(cardname == str(card)):
                return True
        return False

    def showCardSet(self):
        print("Cards in hand:")
        print(self.card_set)

    def showAskOptions(self):
        leftovercards = copy(self.all_cards)
        for card in self.card_set.values:
            leftovercards.remove(card)

        print("Possible options are: " + str(leftovercards))

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