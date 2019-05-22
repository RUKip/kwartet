class Model(object):

    WORLD_KNOWN = 1
    WORLD_MAYBE = 0
    WORLD_DELETED = -1

    group_model = []
    card_model = []
    players = []

    CARD_DEFINITION_LOCATION = "CardDefintions.txt"

    def __init__(self, player_cnt):
        self.players = range(1,player_cnt)

    def generateModel(self):
        file = open(self.CARD_DEFINITION_LOCATION, "r")
        for line in file:
            if line.strip():
                (group, card) = line.split()
                for player in self.players:
                    self.card_model[group][player][card] = self.WORLD_MAYBE
                    self.group_model[group][player] = self.WORLD_MAYBE
                    print("Adding for player " + str(player) + " : group " + group + " - card " + card)
        file.close()
