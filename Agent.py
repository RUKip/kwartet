import logging

from Model import Model


class Agent(object):

	card_set = {}
	opponents = []
	model = None
	id = None
	score = 0

	def __init__(self, id, opponents):
		self.id = id
		self.opponents = opponents

	def makeDecision(self):
		return self.model.getPossiblity(self.card_set)

	def generateInitialModel(self, init_card_set):
		# Set agent's card to WORLD_DELETED.
		# Then we will update model based on init_card_set
		for card_group in iter(self.model.card_model):
			for card in iter(self.model.card_model[card_group][self.id]):
				self.model.card_model[card_group][self.id][card] = Model.WORLD_DELETED
			self.model.group_model[card_group][self.id] = Model.WORLD_DELETED

		self.card_set = init_card_set
		for group in self.card_set:
			# Update model based on the cards own by Agent
			for card in self.card_set[group]:
				self.set_group_for_player(card, self.id, Model.WORLD_KNOWN)
				self.set_card_for_player(card, self.id, Model.WORLD_KNOWN)
				for opponent_id in self.opponents:
					self.set_card_for_player(card, opponent_id, Model.WORLD_DELETED)
				self.checkKwartet(card)

	def askCard(self):
		(card,player) = self.model.getPossiblity(self.card_set)
		return (card,player)

	def giveCard(self, card):
		self.card_set[card.getGroup()].append(card)
		self.set_card_for_player(card, self.id, Model.WORLD_DELETED)
		# TODO: check if group should be deleted as well..
		# self.model.card_model
		# self.model.setGroupForPlayer(card, self.id, Model.WORLD_DELETED)
		self.checkKwartet(card)

	def removeCard(self, card):
		self.card_set[card.getGroup()].remove(card)

	# TODO: do something with model
	# This implements the strategy and knowledge based on the announcement
	def AnnouncementGaveCard(self, card, asker, asked):
		return None

	# TODO: do something with model
	# This implements the strategy and knowledge based on the announcement
	def AnnouncementNotCard(self, card, asker, asked):
		return None

	def setModel(self, model):
		self.model = model
		self.model.players.remove(self.id)

	def getScore(self):
		return self.score

	# TODO: notify all other players that cards are gone could speed up their decision making but not required
	def checkKwartet(self, latest_added_card):
		if (len(self.card_set[latest_added_card.getGroup()]) > 3):
			logging.info("Kwartet! Player " + self.id + " found 4 cards of group " + latest_added_card.getGroup())
			self.set_group_for_player(latest_added_card, self.id, Model.WORLD_DELETED)
			for card in self.card_set[latest_added_card.getGroup()]:
				self.removeCard(card)
			self.score += 1

	def set_card_for_player(self, card, player_id, operator):
		self.model.card_model[card.getGroup()][player_id][card.getCard()] = operator

	def set_group_for_player(self, card, player_id, operator):
		self.model.group_model[card.getGroup()][player_id] = operator
