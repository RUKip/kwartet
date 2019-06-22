import logging

from abc import ABC, abstractmethod

from Card import Card

class Agent(ABC):
    card_set = {}
    opponents = []
    model = None
    id = None
    score = 0
    all_cards = {}

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

    def getScore(self):
        return self.score

    def setAllCards(self, all_cards):
        self.all_cards = all_cards

    def getAllCards(self):
        return self.all_cards

    def getOptions(self):
        options = []
        for card in self.all_cards:
            card = Card(card[0], card[1])
            if len(self.card_set[card.getGroup()]) > 0:
                if not (card in self.card_set[card.getGroup()]):
                    options.append(card)
        return options

    def checkKwartet(self):
        kwarter_group = []
        for group in self.card_set:
            if len(self.card_set[group]) > 3:
                logging.info("Kwartet! Player " + str(self.id) +
                             " found 4 cards of group " +
                             str(group))
                kwarter_group.append(str(group))
        return kwarter_group

    @abstractmethod
    def sorrowPlayer(self, dead_player_id):
        pass

    @abstractmethod
    def AnnouncementGaveCard(self, card, asker_id, asked_id):
        pass

    @abstractmethod
    def AnnouncementNotCard(self, card, asker_id, asked_id):
        pass

    @abstractmethod
    def AnnouncementKwartet(self, group):
        pass

    @abstractmethod
    def basic_thinking(self):
        pass

    @abstractmethod
    def isHuman(self):
        pass
