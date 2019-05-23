from Model import Model


class Agent(object):

	card_set = []
	model = None
	id = None

	def __init__(self,id):
		self.id = id

	def makeDecision(self):
		card = None
		return card

	def generateInitialModel(self, player_count, init_card_set):
		card_set = init_card_set
		for card in card_set:
			self.model.removeCard(card)

	def askCard(self):
		(card,player) = self.model.getPossiblity(self.card_set)
		return (card,player)

	#TODO: do something with model
	def giveCard(self, card):
		self.model

	def setModel(self, model):
		self.model = model