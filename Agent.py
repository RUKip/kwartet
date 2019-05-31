import logging

from Model import Model
from Card import Card
import random


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
		return self.getPossiblity()

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
		# self.set_group_for_player(card, self.id, Model.WORLD_DELETED)
		self.checkKwartet(card)

	def removeCard(self, card):
		self.card_set[card.getGroup()].remove(card)

	# TODO: do something with model
	# This implements the strategy and knowledge based on the announcement
	def AnnouncementGaveCard(self, card, asker_id, asked_id):
		# TODO: some work here..
		self.set_group_for_player(card, asked_id, Model.WORLD_MAYBE)
		self.set_card_for_player(card, asker_id, Model.WORLD_KNOWN)
		self.set_group_for_player(card, asker_id, Model.WORLD_KNOWN)
		for opponent in self.opponents:
			if(not(opponent == asker_id)):
				self.set_card_for_player(card, opponent, Model.WORLD_DELETED)

	# TODO: do something with model
	# This implements the strategy and knowledge based on the announcement
	def AnnouncementNotCard(self, card, asker_id, asked_id):
		self.set_card_for_player(card, asker_id, Model.WORLD_DELETED)
		self.set_group_for_player(card, asker_id, Model.WORLD_KNOWN)
		self.set_card_for_player(card, asked_id, Model.WORLD_DELETED)

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

	def getPossiblity(self):
		known_groups, possible_groups = self.getGroupOptions()

		logging.info("Player card set: " + str(self.card_set))
		logging.info("Known groups: " + str(known_groups))
		logging.info("Possible groups: " + str(possible_groups))

		# prioritize known groups
		if known_groups:
			known_cards, possible_cards = self.getCardOptions(known_groups)
			logging.info("Known group - Known cards: " + str(known_cards))
			logging.info("Known group - Possible cards: " + str(possible_cards))

			if known_cards:
				return random.choice(known_cards)  # ask a know card
			elif possible_cards:
				return random.choice(possible_cards)  # ask a possible card with know group
			raise Exception("Something went wrong, detected a group but no cards available in that group!")

		if possible_groups:
			# If card is known, group is known so no option of known_card in possible group
			_, possible_cards = self.getCardOptions(possible_groups)
			logging.info("Possible group - Possible cards: " + str(possible_cards))
			if possible_cards:
				return random.choice(possible_cards)  # ask a possible card
		return (None, None)  # no more options

	def getGroupOptions(self):
		known_groups = []
		possible_groups = []
		for group in self.card_set:
			for card in self.card_set[group]:
				for player in self.model.players:
					if self.model.group_model[card.getGroup()][player] == self.model.WORLD_KNOWN:
						known_groups.append((card.getGroup(), player))
					elif self.model.group_model[card.getGroup()][player] == self.model.WORLD_MAYBE:
						possible_groups.append((card.getGroup(), player))
		return known_groups, possible_groups

	def getCardOptions(self, agent_groups):
		known_cards = []
		possible_cards = []
		for (group, player) in agent_groups:
			for card in self.model.card_model[group][player]:
				if self.model.card_model[group][player][card] == self.model.WORLD_KNOWN:
					known_cards.append((Card(group, card), player))
				elif self.model.card_model[group][player][card] == self.model.WORLD_MAYBE:
					possible_cards.append((Card(group, card), player))
		return known_cards, possible_cards
