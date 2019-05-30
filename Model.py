import os
import logging

from Card import Card
import random

class Model(object):

    WORLD_KNOWN = 1     #Equal to K operator
    WORLD_MAYBE = 0     #Equal to M operator
    WORLD_DELETED = -1  #Equal to being removed

    group_model = {}    #Model of group options
    card_model = {}     #Full model of card options
    players = []        #Players id's excluding self
    owner = None        #Owner of this model

    CARD_DEFINITION_LOCATION = "CardDefinitions.txt"

    def __init__(self, player_cnt):
        self.players = list(range(1,player_cnt+1))

    def initModel(self):
        file = open(os.path.dirname(os.path.abspath(__file__)) + "/" + self.CARD_DEFINITION_LOCATION, "r")
        for line in file:
            if line.strip():
                (group, card) = line.split()
                for player in self.players:
                    if(not group in self.card_model):
                        self.card_model[group] = {}
                    if (not player in self.card_model[group]):
                        self.card_model[group][player] = {}
                    self.card_model[group][player][card] = self.WORLD_MAYBE

                    if (not group in self.group_model):
                        self.group_model[group] = {}
                    self.group_model[group][player] = self.WORLD_MAYBE

        #print("Initial group model: " + str(self.group_model)) #debug
        #print("Initial card model: " + str(self.card_model)) #debug
        file.close()

    #returns tuple (Card card, int player_id)
    def getPossiblity(self, card_set):
        known_groups, possible_groups = self.getGroupOptions(card_set)

        logging.info("Card set: " + str(card_set))
        logging.info("Possible groups: " + str(possible_groups) + ", known groups: " + str(known_groups))

        #prioritize known groups
        if known_groups:
            known_cards, possible_cards = self.getCardOptions(known_groups)
            logging.info("Known group - Possible cards: " + str(possible_cards) + ", known cards: " + str(known_cards))

            if known_cards:
                return random.choice(known_cards)       #ask a know card
            elif possible_cards:
                return random.choice(possible_cards)    #ask a possible card with know group
            raise Exception("Something went wrong, detected a group but no cards available in that group!")

        if possible_groups:
            _ , possible_cards = self.getCardOptions(possible_groups) #if card is known, group is known so no option of known_card in possible group
            logging.info("Possible group - Possible cards: " + str(possible_cards))
            if possible_cards:
                return random.choice(possible_cards)    #ask a possible card
        return (None, None) #no more options

    def getGroupOptions(self, card_set):
        known_groups = []
        possible_groups = []
        for group in card_set:
            for card in card_set[group]:
                for player in self.players:
                    if (self.group_model[card.getGroup()][player] == self.WORLD_KNOWN):
                        known_groups.append((card.getGroup(), player))
                    elif (self.group_model[card.getGroup()][player] == self.WORLD_MAYBE):
                        possible_groups.append((card.getGroup(), player))
        return (known_groups, possible_groups)

    def getCardOptions(self, agent_groups):
        known_cards = []
        possible_cards = []
        for (group, player) in agent_groups:
            for card in self.card_model[group][player]:
                if (self.card_model[group][player][card] == self.WORLD_KNOWN):
                    known_cards.append((Card(group,card), player))
                elif (self.card_model[group][player][card] == self.WORLD_MAYBE):
                    possible_cards.append((Card(group,card), player))
        return (known_cards, possible_cards)

    def setCardForPlayer(self, card, player_id, operator):
        self.card_model[card.getGroup()][player_id][card.getCard()] = operator

    def setGroupForPlayer(self, group, player_id, operator):
            self.group_model[group][player_id] = operator

    def setOwner(self, owner):
        if(self.owner is None):
            self.owner = owner
            self.players.remove(owner.id)
            # make sure the agent cant ask himself! by removing him from the model
            for group in self.group_model:
                self.setGroupForPlayer(group, owner.id, self.WORLD_DELETED)
                for card in self.card_model[group][owner.id]:
                    self.setCardForPlayer(Card(group,card), owner.id, self.WORLD_DELETED)
        else:
            raise Exception("Model already has an owner!")