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
    players = []        #Players id's excluding self
    # owner = None        #Owner of this model

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

        logging.debug("Initial group model: " + str(self.group_model))
        logging.debug("Initial card model: " + str(self.card_model))
        file.close()
