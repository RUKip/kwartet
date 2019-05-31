class Card(object):

    def __init__(self, group, card_name):
        self.group = group
        self.card_name = card_name

    def getGroup(self):
        return self.group

    def getCard(self):
        return self.card_name

    def __eq__(self, other):
        if (self.card_name == other.card_name) and (self.group == other.group):
            return True
        else:
            return False

    def __str__(self):
        return self.group + ":" + self.card_name

    def __repr__(self):
        return self.group + ":" + self.card_name
