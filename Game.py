from Agent import Agent
from Model import Model

class Game(object):

    agents = []
    cards_in_play = {}

    def initGame(self):
        player_cnt = None
        while player_cnt is None:
            try:
                player_cnt = int(input("How many players?: "))
            except:
                print("Not valid, try a different number")
                pass

        model = Model(player_cnt)
        model.initModel()

        for agent in range(1, player_cnt+1):
            self.agents.append(Agent())

        

    def startGame(self):
        return None
        #do some random division of cards here
