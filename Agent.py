import logging

from abc import ABC, abstractmethod

class Agent(ABC):
    card_set = {}
    opponents = []
    model = None
    id = None
    score = 0

    def __init__(self, id, opponents):
        self.id = id
        self.opponents = opponents

    def __eq__(self, other):
        if ((self.card_set == other.card_set) and
                (self.opponents == other.opponents) and
                (self.model == other.model) and
                (self.id == other.id) and
                (self.score == other.score)):
            return True
        else:
            return False

    @abstractmethod
    def makeDecision(self):
        pass

    @abstractmethod
    def generateInitialModel(self, init_card_set):
        pass

    def giveCard(self, card):
        self.card_set[card.getGroup()].append(card)

    def removeCard(self, card):
        self.card_set[card.getGroup()].remove(card)

    def remove_group(self, group):
        self.card_set[group].clear()

    def setModel(self, model):
        self.model = model
        self.model.players.remove(self.id)

    def getScore(self):
        return self.score

    def checkKwartet(self):
        kwarter_group = []
        for group in self.card_set:
            if len(self.card_set[group]) > 3:
                logging.info("Kwartet! Player " + str(self.id) +
                             " found 4 cards of group " +
                             str(group))
                kwarter_group.append(str(group))
        return kwarter_group

    # We just need to delete group model as this is vital to picking from card_model
    @abstractmethod
    def sorrowPlayer(self, dead_player_id):
        pass
