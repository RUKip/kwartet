class Card(object):

    def __init__(self, group, card_name, owner):
        self.group = group
        self.card_name = card_name

    def getGroup(self):
        return self.group

    def getCard(self):
        return self.card_name