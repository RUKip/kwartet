class Agent(object):

	card_set = []
	model = null

	def makeDecision(self):
		card = null
		return card

	def generateInitialWorld(self, player_count, init_card_set):
		card_set = init_card_set
		model = generateModel()
		for card in card_set:
			model.removeCard(card)

	def askCard(self):
		(card,player) = model.getPossiblity()
		return (card,player)
