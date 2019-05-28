class Card(object):

    def __init__(self, group, card_name):
        self.group = group
        self.card_name = card_name

    def getGroup(self):
        return self.group

    def getCard(self):
        return self.card_name

    def __str__(self):
        return self.group + ":" + self.card_name

    def __repr__(self):
        return self.group + ":" + self.card_name