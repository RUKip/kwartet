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

	def __eq__(self, other):
		if ((self.card_set == other.card_set) and
				(self.opponents == other.opponents) and
				(self.model == other.model) and
				(self.id == other.id) and
				(self.score == other.score)):
			return True
		else:
			return False

	def makeDecision(self):
		if self.id == 1:
			return self.askRandom()
		else:
			return self.askKnownCards()

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

	# ~ def askCard(self):
		# ~ (card,player) = self.model.askKnownCards(self.card_set)
		# ~ return (card,player)

	def giveCard(self, card):
		self.card_set[card.getGroup()].append(card)

	def removeCard(self, card):
		self.card_set[card.getGroup()].remove(card)

	def remove_group(self, group):
		self.card_set[group].clear()
		self.model.group_model[group][self.id] = Model.WORLD_DELETED
		for card in self.model.card_model[group][self.id]:
			self.set_card_for_player(Card(group, card), self.id, Model.WORLD_DELETED)

	def AnnouncementGaveCard(self, card, asker_id, asked_id):
		"""
		After the announcement that player(asked_id) has the card, we update
		the agent's model. We now know that the player(asker_id) has the
		requested card and the requested card's group. We also know that the
		player(asked_id) doesn't have the card anymore, but not sure if he still
		has cards from that group.

		Args:
			card: requested card
			asker_id: player that requested the card
			asked_id: player that was requested the card

		Returns:
			Nothing

		"""
		# Updating model for the player(asked_id)
		self.set_card_for_player(card, asked_id, Model.WORLD_DELETED)
		self.set_group_for_player(card, asked_id, Model.WORLD_MAYBE)
		# Updating model for the player(asker_id)
		self.set_card_for_player(card, asker_id, Model.WORLD_KNOWN)
		self.set_group_for_player(card, asker_id, Model.WORLD_KNOWN)

	def AnnouncementNotCard(self, card, asker_id, asked_id):
		"""
		After the announcement that player(asked_id) does not have a card,
		we update the agent's model. We know that player(asker_id) has the
		group of the requested card. We know that player(asked_id) doesn't have
		that card.

		Args:
			card: requested card
			asker_id: player that requested the card
			asked_id: player that was requested the card

		Returns:
			Nothing
		"""
		# Updating model for the player(asked_id)
		self.set_card_for_player(card, asked_id, Model.WORLD_DELETED)
		# Updating model for the player(asker_id)
		self.set_group_for_player(card, asker_id, Model.WORLD_KNOWN)
		self.set_card_for_player(card, asker_id, Model.WORLD_DELETED)

	def AnnouncementKwartet(self, group):
		"""
		This announcement is done after a player gather 4 cards of same type (Kwartet).
		The other players know that cards belonging to that group are not possible anymore

		Args:
			group: card group

		Returns:
			Nothing

		"""
		# Delete cards and group from own model
		# Shouldn't be necessary, bc they should already be set to deleted,
		# but just in case... also, this would be useful if we implement forgetting.
		self.model.group_model[group][self.id] = Model.WORLD_DELETED
		for card in self.model.card_model[group][self.id]:
			self.set_card_for_player(Card(group, card), self.id, Model.WORLD_DELETED)
		# Delete cards and group from opponents models
		for opponent in self.opponents:
			self.model.group_model[group][opponent] = Model.WORLD_DELETED
			for card in self.model.card_model[group][opponent]:
				self.set_card_for_player(Card(group, card), opponent, Model.WORLD_DELETED)

	def basic_thinking(self):
		"""
		This function simulates basic reasoning that each agent should follow.
		Such that 'if I know that I have a card, I know others don't'

		Args:
			player_cards: cards belonging to agent

		Returns:
			Nothing

		"""
		# Go through our own cards. Set to deleted those cards in rest of the players's models
		player_cards = self.card_set
		for group in player_cards:
			for card in player_cards[group]:
				for player_id in self.model.players:
					self.set_card_for_player(card, player_id, Model.WORLD_DELETED)
		# Go through everyone's card status. If anybody has 4 Model.WORLD_DELETED, then group deleted.
		for group in self.model.card_model.keys():
			for player in self.model.card_model[group].keys():
				aux = sum(self.model.card_model[group][player].values())
				if aux == -4:
					self.model.group_model[group][player] = self.model.WORLD_DELETED

	def advanced_thinking(self):
		"""
		This function simulates more advanced reasoning. Here we could implement
		guesses on other player's status. This way we could compare how players
		with different strategies (basic vs. advanced) perform.

		Returns:
			Nothing

		"""
		msg = "Player " + str(self.id) + " does not yet have advanced strategies implemented at the moment.."
		logging.debug(msg)

		# TODO: if time permits it do some more advanced strategies
		# E.g. if I am certain that numplayers-1 don't have a card then I know
		# who has the card

		# E.g. if, I know that a player has a card, then I also know that the
		# others dont't have it, so adapt model consequently

	def setModel(self, model):
		self.model = model
		self.model.players.remove(self.id)

	def getScore(self):
		return self.score

	def checkKwartet(self):
		kwarter_group = []
		for group in self.card_set:
			if len(self.card_set[group]) > 3:
				logging.info("Kwartet! Player " + str(self.id) +
							 " found 4 cards of group " +
							 str(group))
				kwarter_group.append(str(group))
		return kwarter_group

	def set_card_for_player(self, card, player_id, operator):
		self.model.card_model[card.getGroup()][player_id][card.getCard()] = operator

	def set_group_for_player(self, card, player_id, operator):
		self.model.group_model[card.getGroup()][player_id] = operator

	def askRandom(self):
		logging.info("Player %d will ask for a random possible card." %self.id)
		logging.info("Player card set: " + str(self.card_set))

		possible_cards = []
		for group in self.card_set:
			if self.card_set[group]:	# player is allowed to ask for a card in this group
				for player in self.opponents:
					for card in self.model.card_model[group][player]:
						if self.model.card_model[group][player][card] == self.model.WORLD_KNOWN:
							possible_cards.append((Card(group, card), player))
						if self.model.card_model[group][player][card] == self.model.WORLD_MAYBE:
							possible_cards.append((Card(group, card), player))

		if possible_cards:
			logging.info("Possible cards: " + str(possible_cards))
			return random.choice(possible_cards)  # ask a possible card
		else:
			aux = False
			# check if player still has cards
			for group in self.card_set.keys():
				if len(self.card_set[group]) > 0:
					aux = True
					break
			if aux:
				logging.debug("There is some confusion. there are some possible groups but no possible cards.")
				# If our current knowledge model tells us that players don't have cards or groups, but we still have cards
				avail_groups = []  # groups that could be requested
				for group in self.card_set.keys():
					if len(self.card_set[group]) > 0:
						avail_groups.append(group)
				rand_group = random.choice(avail_groups)
				avail_cards = []  # cards that we do not own
				for card in self.model.card_model[rand_group][self.id].keys():
					if self.model.card_model[rand_group][self.id][card] == Model.WORLD_DELETED:
						avail_cards.append(card)
				rand_card = random.choice(avail_cards)
				rand_player = random.choice(self.opponents)
				return Card(rand_group, rand_card), rand_player
			else:
				return (None, None)  # no more options

	def askKnownCards(self):
		known_groups, possible_groups = self.getGroupOptions()

		logging.info("Player card set: " + str(self.card_set))
		logging.info("Known groups: " + str(known_groups))
		logging.info("Possible groups: " + str(possible_groups))

		possible_cards = []
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

		elif possible_groups:
			# If card is known, group is known so no option of known_card in possible group
			_, possible_cards = self.getCardOptions(possible_groups)
			logging.info("Possible group - Possible cards: " + str(possible_cards))

		if possible_cards:
			return random.choice(possible_cards)  # ask a possible card

		else:
			aux = False
			# check if player still has cards
			for group in self.card_set.keys():
				if len(self.card_set[group]) > 0:
					aux = True
					break
			if aux:
				logging.debug("There is some confusion. there are some possible groups but no possible cards.")
				# If our current knowledge model tells us that players don't have cards or groups, but we still have cards
				avail_groups = []  # groups that could be requested
				for group in self.card_set.keys():
					if len(self.card_set[group]) > 0:
						avail_groups.append(group)
				rand_group = random.choice(avail_groups)
				avail_cards = []  # cards that we do not own
				for card in self.model.card_model[rand_group][self.id].keys():
					if self.model.card_model[rand_group][self.id][card] == Model.WORLD_DELETED:
						avail_cards.append(card)
				rand_card = random.choice(avail_cards)
				rand_player = random.choice(self.opponents)
				return Card(rand_group, rand_card), rand_player
			else:
				return (None, None)  # no more options

	def getGroupOptions(self):
		known_groups = []
		possible_groups = []
		for group in self.card_set:
			if self.card_set[group]:
				for player in self.model.players:
					if self.model.group_model[group][player] == self.model.WORLD_KNOWN:
						known_groups.append((group, player))
					elif self.model.group_model[group][player] == self.model.WORLD_MAYBE:
						possible_groups.append((group, player))
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

	# We just need to delete group model as this is vital to picking from card_model
	def sorrowPlayer(self, dead_player_id):
		for group in self.model.group_model:
			for player in self.model.group_model[group]:
				if player == dead_player_id:
					self.model.group_model[group][player] = Model.WORLD_DELETED
		logging.info("Player " + str(self.id) + " now knows player " + str(dead_player_id) + " sleeps with the fishes. RIP")
