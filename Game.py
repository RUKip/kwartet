from Model import Model

class Game(object):

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


    def startGame(self):
        return None
        #do some random division of cards here
