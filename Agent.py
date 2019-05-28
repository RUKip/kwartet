from Model import Model

class Agent(object):

	card_set = []
	model = None
	id = None
	score = 0

	def __init__(self,id):
		self.id = id

	def makeDecision(self):
		return self.model.getPossiblity(self.card_set)

	def generateInitialModel(self, init_card_set):
		self.card_set = init_card_set
		for card in self.card_set:
			self.model.removeCard(card, self.id)

	def askCard(self):
		(card,player) = self.model.getPossiblity(self.card_set)
		return (card,player)

	def giveCard(self, card, from_player):
		self.card_set.append(card)
		self.AnnouncementGaveCard(card, self.id, from_player)

	def removeCard(self, card, to_player):
		self.card_set.remove(card)
		self.AnnouncementGaveCard(card, to_player, self.id)

	#TODO: do something with model
	def AnnouncementGaveCard(self, card, asker, asked):
		return None

	#TODO: do something with model
	def AnnouncementNotCard(self, card, asker, asked):
		return None

	def setModel(self, model):
		self.model = model
		self.model.setOwner(self)

	def getScore(self):
		return self.score