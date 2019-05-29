import os

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

        print("Initial group model: " + str(self.group_model))
        print("Initial card model: " + str(self.card_model))
        file.close()

    #returns tuple (Card card, int player_id)
    def getPossiblity(self, card_set):
        known_groups = []
        possible_groups = []
        print("Player possiblities: " + str(self.players))
        for card in card_set:
            for player in self.players:
                print("State of card: " + str(card)  + " for player " + str(player) +  " is: " + str(self.group_model[card.getGroup()][player]))
                if(self.group_model[card.getGroup()][player] == self.WORLD_KNOWN):
                    known_groups.append((card.getGroup(), player))
                elif(self.group_model[card.getGroup()][player] == self.WORLD_MAYBE):
                    possible_groups.append((card.getGroup(),player))

        print("Card set: " + str(card_set))
        print("Possible groups: " + str(possible_groups) + ", known groups: " + str(known_groups))

        known_cards = []
        possible_cards = []
        #prioritize known groups
        if known_groups:
            for (group,player) in known_groups:
                for card in self.card_model[group][player]:
                    if(self.card_model[group][player][card.getCard()] == self.WORLD_KNOWN):
                        known_cards.append((card,player))
                    elif(self.card_model[group][player][card.getCard()] == self.WORLD_MAYBE):
                        possible_cards.append((card,player))
            if known_cards:
                return random.choice(known_cards)       #ask a know card
            elif possible_cards:
                return random.choice(possible_cards)    #ask a possible card with know group
            raise Exception("Something went wrong, detected a group but no cards available in that group!")

        if possible_groups:
            for (group,player) in possible_groups:
                for card in self.card_model[group][player]:     #if card is known, group is known so no option of known_card in possible group
                    possible_cards.append((Card(group, card), player))
            if possible_cards:
                return random.choice(possible_cards)    #ask a possible card
        return (None, None) #no more options

    def removeCard(self, card, player):
        self.card_model[card.getGroup()][player][card.getCard()] = self.WORLD_DELETED

    def removeGroup(self, group, player):
        self.group_model[group][player] = self.WORLD_DELETED

    def setOwner(self, owner):
        if(self.owner is None):
            self.owner = owner
            self.players.remove(owner.id)
        else:
            raise Exception("Model already has an owner!")