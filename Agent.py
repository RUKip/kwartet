from kwartet.Model import Model


class Agent(object):

	card_set = []
	model = Model()

	def makeDecision(self):
		card = None
		return card

	def generateInitialWorld(self, player_count, init_card_set):
		card_set = init_card_set
		self.model.generateModel()
		for card in card_set:
			self.model.removeCard(card)

	def askCard(self):
		(card,player) = self.model.getPossiblity()
		return (card,player)

	def setModel(self, model):
		self.model = model