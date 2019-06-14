import logging

from Agent import Agent

class HumanAgent(Agent):

    def makeDecision(self):
        logging.info("Human player's turn")
        print("It is your turn!")
        print("Cards in hand:")
        print(self.card_set)
        agent_id = None
        while agent_id is None:
            try:
                agent_id = int(input("Ask which player?"))
                if(agent_id == self.id):
                    raise Exception("Try not asking yourself")
                if(not(agent_id in self.opponents)):
                    raise Exception("Available agents are: " + str(self.opponents.keys()))
            except:
                print("Sorry not valid")
                agent_id = None

        card = None
        while card is None:
            try:
                card = input("Which card? (syntax => group:card_name)")
                group_cardname = card.split(":")
                if(not(len(group_cardname)==2)):
                    Exception("Wrong syntax")
                if(not self.is_valid(group_cardname)):
                    Exception("That is not a card you can ask")
            except:
                print("Sorry not valid")
                card = None

    def generateInitialModel(self, init_card_set):
        self.card_set = init_card_set

    def sorrowPlayer(self, dead_player_id):
        print("Player " + str(dead_player_id) + " sleeps with the fishes")
        self.opponents.pop(dead_player_id)

    def is_valid(self, group_cardname):
        for card in self.card_set.values():
            if card.getGroup() == group_cardname[0]:
                for group_card in self.model[card.getGroup()][0]:
                    if group_card == group_cardname[1]:
                        return True
        return False
