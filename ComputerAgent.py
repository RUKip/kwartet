import logging

from Agent import Agent
from Model import Model
from Card import Card
import random


class ComputerAgent(Agent):

	STRATEGY_RANDOM = 0
	STRATEGY_1ST = 1
	STRATEGY_2ND = 2

	BASIC_THINKING = 0
	ADVANCED_THINKING = 1

	def __init__(self, id, opponents, strategy):
		super().__init__(id, opponents)
		self.strategy = strategy

	#Set strategies for agents here!
	def makeDecision(self):
		if self.strategy == self.STRATEGY_1ST:
			logging.info("Agent " + str(self.id) + ", playing first order")
			return self.askKnownCards()
		elif self.strategy == self.STRATEGY_2ND:
			logging.info("Agent " + str(self.id) + ", playing second order")
			return self.askKnownCardsSecondOrder()
		logging.info("Agent " + str(self.id) + ", playing random")
		return self.askRandom()

	def generateInitialModel(self, init_card_set):
		# Set agent's card to WORLD_DELETED for own observation.
		# Then we will update model based on init_card_set
		for card_group in iter(self.model.card_model):
			for card in iter(self.model.card_model[card_group][self.id][self.id]):
				self.model.card_model[card_group][self.id][self.id][card] = Model.WORLD_DELETED
			self.model.group_model[card_group][self.id][self.id] = Model.WORLD_DELETED

		self.card_set = init_card_set
		for group in self.card_set:
			# Update model based on the cards own by Agent
			for card in self.card_set[group]:
				self.set_group_for_player(card, self.id, self.id, Model.WORLD_KNOWN)
				self.set_card_for_player(card, self.id, self.id, Model.WORLD_KNOWN)
				for opponent_id in self.opponents:
					self.set_card_for_player(card, self.id, opponent_id, Model.WORLD_DELETED)

	def remove_group(self, group):
		self.card_set[group].clear()
		for observer in self.model.players:
			self.model.group_model[group][observer][self.id] = Model.WORLD_DELETED
			for card in self.model.card_model[group][observer][self.id]:
				self.set_card_for_player(Card(group, card), observer, self.id, Model.WORLD_DELETED)


	def AnnouncementGaveCard(self, given_card, asker_id, asked_id):
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
		for observer in self.model.players:
			# Updating model for the player(asked_id)
			self.set_card_for_player(given_card, observer, asked_id, Model.WORLD_DELETED)
			# Check if there is still a known card
			known_cards = 0
			for card in self.model.card_model[given_card.getGroup()][observer][asked_id]:
				if (self.model.card_model[given_card.getGroup()][observer][asked_id][card] == Model.WORLD_KNOWN):
					known_cards += 1
			if (known_cards == 0):
				self.set_group_for_player(given_card, observer, asked_id, Model.WORLD_MAYBE)

			# Updating model for the player(asker_id)
			self.set_card_for_player(given_card, observer, asker_id, Model.WORLD_KNOWN)
			self.set_group_for_player(given_card, observer, asker_id, Model.WORLD_KNOWN)

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
		for observer in self.model.players:
			# Updating model for the player(asked_id)
			self.set_card_for_player(card, observer, asked_id, Model.WORLD_DELETED)
			# Updating model for the player(asker_id)
			self.set_group_for_player(card, observer, asker_id, Model.WORLD_KNOWN)
			self.set_card_for_player(card, observer, asker_id, Model.WORLD_DELETED)

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
		self.model.group_model[group][self.id][self.id] = Model.WORLD_DELETED
		for card in self.model.card_model[group][self.id][self.id]:
			self.set_card_for_player(Card(group, card), self.id, self.id, Model.WORLD_DELETED)
		# Delete cards and group from model (to update output graph model)
		for observer in self.model.players:
			for player in self.model.players:
				self.model.group_model[group][observer][player] = Model.WORLD_DELETED
				for card in self.model.card_model[group][observer][player]:
					self.set_card_for_player(Card(group, card), observer, player, Model.WORLD_DELETED)


	def basic_thinking(self):
		"""
		This function simulates basic reasoning that each agent should follow.
		Such that 'if I know that I have a card, I know others don't'

		Args:
			player_cards: cards belonging to agent

		Returns:
			Nothing

		"""
		logging.info("Agent " + str(self.id) + " applies basic thinking")
		# Go through our own cards. Set to deleted those cards in rest of the players's models
		player_cards = self.card_set
		for group in player_cards:
			for card in player_cards[group]:
				for opponent in self.opponents:
					self.set_card_for_player(card, self.id, opponent, Model.WORLD_DELETED)

	def advanced_thinking(self):
		"""
		This function simulates more advanced reasoning. Here we could implement
		guesses on other player's status. This way we could compare how players
		with different strategies (basic vs. advanced) perform.

		Returns:
			Nothing

		"""
		
		logging.info("Agent " + str(self.id) + " applies advanced thinking")
		
		# Go through opponents card status. If someone has a card, the other players do not have this card.
		for group in self.model.card_model.keys():
			for observer in self.model.players:
				for card in self.model.card_model[group][observer][self.id]:
					for opponent in self.opponents:
						if self.model.card_model[group][observer][opponent][card] == Model.WORLD_KNOWN:
							for other_player in self.opponents:
								if other_player != opponent:
									self.model.card_model[group][observer][other_player][card] = Model.WORLD_DELETED
		
		# Go through everyones card status. If all but one do not have the card, the other player does have this card.
		for group in self.model.card_model.keys():
			for observer in self.model.players:
				for card in self.model.card_model[group][observer][self.id]:
					deleted_cards = 0
					stored_player = None
					for player in self.model.players:
						if self.model.card_model[group][observer][player][card] == Model.WORLD_DELETED:
							deleted_cards += 1
						else:
							if(stored_player is None):
								stored_player = player
							else:
								return
					if (deleted_cards == (len(self.model.players) - 1)):
						self.model.card_model[group][observer][stored_player][card] = Model.WORLD_KNOWN
						self.model.group_model[group][observer][stored_player] = Model.WORLD_KNOWN

	def set_card_for_player(self, card, observer, player_id, operator):
		self.model.card_model[card.getGroup()][observer][player_id][card.getCard()] = operator

	def set_group_for_player(self, card, observer, player_id, operator):
		self.model.group_model[card.getGroup()][observer][player_id] = operator

	def askRandom(self):
		logging.info("Player %d will ask for a random possible card." %self.id)
		logging.info("Player card set: " + str(self.card_set))
		options = self.getOptions()
		if options and self.opponents:
			random_card = random.choice(options)
			random_player = random.choice(self.opponents)
			return	(random_card, random_player)
		return (None,None)

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
				for card in self.model.card_model[rand_group][self.id][self.id].keys():
					if self.model.card_model[rand_group][self.id][self.id][card] == Model.WORLD_DELETED:
						avail_cards.append(card)
				rand_card = random.choice(avail_cards)
				rand_player = random.choice(self.opponents)
				return Card(rand_group, rand_card), rand_player
			else:
				return (None, None)  # no more options

	def askKnownCardsSecondOrder(self):
		'''
		This function asks for known cards of which opponents already 
		know we have something of that group
		'''
		
		knownop_known_groups = []
		knownop_possible_groups = []
		known_groups = []
		possible_groups = []
		for group in self.card_set:
			if self.card_set[group]:
				for player in self.opponents:
					if self.model.group_model[group][self.opponents[0]][self.id] == self.model.WORLD_KNOWN:
						if self.model.group_model[group][self.id][player] == self.model.WORLD_KNOWN:
							knownop_known_groups.append((group, player))
						elif self.model.group_model[group][self.id][player] == self.model.WORLD_MAYBE:
							knownop_possible_groups.append((group, player))
					else:
						if self.model.group_model[group][self.id][player] == self.model.WORLD_KNOWN:
							known_groups.append((group, player))
						elif self.model.group_model[group][self.id][player] == self.model.WORLD_MAYBE:
							possible_groups.append((group, player))
							
		logging.info("Player card set: " + str(self.card_set))
		logging.info("Known by opponents, known groups: " + str(knownop_known_groups))
		logging.info("Known by opponents, possible groups: " + str(knownop_possible_groups))
		logging.info("Unknown by opponents, known groups: " + str(known_groups))
		logging.info("Unknown by opponents, possible groups: " + str(possible_groups))

		possible_cards = []
		# prioritize known groups
		if knownop_known_groups:
			known_cards, possible_cards = self.getCardOptions(knownop_known_groups)

			logging.info("Known by opponents, known group - Known cards: " + str(known_cards))
			logging.info("Known by opponents, known group - Possible cards: " + str(possible_cards))

			if known_cards:
				return random.choice(known_cards)  # ask a know card
			elif possible_cards:
				return random.choice(possible_cards)  # ask a possible card with know group
			raise Exception("Something went wrong, detected a group but no cards available in that group!")
		elif knownop_possible_groups:
			_, possible_cards = self.getCardOptions(knownop_possible_groups)
			logging.info("Known by opponents, possible group - Possible cards: " + str(possible_cards))
			
			if possible_cards:
				return random.choice(possible_cards)  # ask a possible card with know group
			raise Exception("Something went wrong, detected a group but no cards available in that group!")
		elif known_groups:
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
				for card in self.model.card_model[rand_group][self.id][self.id].keys():
					if self.model.card_model[rand_group][self.id][self.id][card] == Model.WORLD_DELETED:
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
				for player in self.opponents:
					if self.model.group_model[group][self.id][player] == self.model.WORLD_KNOWN:
						known_groups.append((group, player))
					elif self.model.group_model[group][self.id][player] == self.model.WORLD_MAYBE:
						possible_groups.append((group, player))
		return known_groups, possible_groups

	def getCardOptions(self, agent_groups):
		known_cards = []
		possible_cards = []
		for (group, player) in agent_groups:
			for card in self.model.card_model[group][self.id][player]:
				if self.model.card_model[group][self.id][player][card] == self.model.WORLD_KNOWN:
					known_cards.append((Card(group, card), player))
				elif self.model.card_model[group][self.id][player][card] == self.model.WORLD_MAYBE:
					possible_cards.append((Card(group, card), player))
		return known_cards, possible_cards

	# We just need to delete group model as this is vital to picking from card_model
	def sorrowPlayer(self, dead_player_id):
		for group in self.model.group_model:
			for observer in self.model.group_model[group]:
				for player in self.model.group_model[group][observer]:
					if player == dead_player_id:
						self.model.group_model[group][observer][player] = Model.WORLD_DELETED
						self.model.card_model[group][observer][player] = Model.WORLD_DELETED
		
		# remove player from game
		if dead_player_id in self.model.players:
			self.model.players.remove(dead_player_id)
		if dead_player_id in self.opponents:
			self.opponents.remove(dead_player_id)
		 
		logging.info("Player " + str(self.id) + " now knows player " + str(dead_player_id) + " sleeps with the fishes. RIP")
		
	def isHuman(self):
		return False
