import os

class Model(object):

    WORLD_KNOWN = 1
    WORLD_MAYBE = 0
    WORLD_DELETED = -1

    group_model = {}
    card_model = {}
    players = []

    CARD_DEFINITION_LOCATION = "CardDefinitions.txt"

    def __init__(self, player_cnt):
        self.players = range(1,player_cnt+1)

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
