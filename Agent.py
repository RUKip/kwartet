from Model import Model

class Agent(object):

	card_set = {}
	playersg =
	model = None
	id = None
	score = 0

	def __init__(self,id):
		self.id = id

	def makeDecision(self):
		return self.model.getPossiblity(self.card_set)

	def generateInitialModel(self, init_card_set):
		self.card_set = init_card_set
		for group in self.card_set:
			for card in self.card_set[group]:
				self.model.setCard(card, self.id, Model.WORLD_DELETED)
				self.checkKwartet(card)
		print("Card model for agent " + str(self.id) + " : " + str(self.model.card_model))

	def askCard(self):
		(card,player) = self.model.getPossiblity(self.card_set)
		return (card,player)

	def giveCard(self, card):
		self.card_set[card.getGroup()].append(card)
		self.model.setGroup(card, self.id, Model.WORLD_DELETED)
		self.checkKwartet(card)

	def removeCard(self, card):
		self.card_set[card.getGroup()].remove(card)

	#TODO: do something with model
	#This implements the strategy and knowledge based on the announcement
	def AnnouncementGaveCard(self, card, asker, asked):
		return None

	#TODO: do something with model
	#This implements the strategy and knowledge based on the announcement
	def AnnouncementNotCard(self, card, asker, asked):
		return None

	def setModel(self, model):
		self.model = model
		self.model.setOwner(self)

	def getScore(self):
		return self.score

	#TODO: notify all other players that cards are gone could speed up their decision making but not required
	def checkKwartet(self, latest_added_card):
		if (len(self.card_set[latest_added_card.getGroup()]) > 3):
			print("Kwartet! Found 4 cards of group " + latest_added_card.getGroup())
			self.model.setGroup(latest_added_card.getGroup(), self, Model.WORLD_DELETED)
			for card in self.card_set[latest_added_card.getGroup()]:
				self.removeCard(card)
			self.score += 1
