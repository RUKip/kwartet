import os
import logging
import copy

from Card import Card
import random


class Model(object):

    WORLD_KNOWN = 1     #Equal to K operator
    WORLD_MAYBE = 0     #Equal to M operator
    WORLD_DELETED = -1  #Equal to being removed

    group_model = {}    #Model of group options
    card_model = {}     #Full model of card options
    
    players = []        #Players id's still in the game

    CARD_DEFINITION_LOCATION = "CardDefinitions.txt"

    def __init__(self, player_cnt):
        self.players = list(range(1,player_cnt+1))

    def __deepcopy__(self, memodict={}):
        newone = type(self)(len(self.players))
        newone.__dict__.update(self.__dict__)
        newone.group_model = copy.deepcopy(self.group_model, memodict)
        newone.card_model = copy.deepcopy(self.card_model, memodict)
        newone.players = copy.deepcopy(self.players, memodict)
        return newone

    def __eq__(self, other):
        if ((self.group_model == other.group_model) and
                (self.card_model == other.card_model) and
                (self.players == self.players)):
            return True
        else:
            return False

    def initModel(self):
        file = open(os.path.dirname(os.path.abspath(__file__)) + "/" + self.CARD_DEFINITION_LOCATION, "r")
        for line in file:
            if line.strip():
                (group, card) = line.split()
                for observer in self.players:
                    for player in self.players:
                        # initialize fields
                        if (not group in self.card_model):
                            self.card_model[group] = {}
                        if (not observer in self.card_model[group]):
                            self.card_model[group][observer] = {}
                        if (not player in self.card_model[group][observer]):
                            self.card_model[group][observer][player] = {}
                        self.card_model[group][observer][player][card] = self.WORLD_MAYBE

                        if (not group in self.group_model):
                            self.group_model[group] = {}
                        if (not observer in self.group_model[group]):
                            self.group_model[group][observer] = {}
                        self.group_model[group][observer][player] = self.WORLD_MAYBE

        logging.debug("Initial group model: " + str(self.group_model))
        logging.debug("Initial card model: " + str(self.card_model))
        file.close()
