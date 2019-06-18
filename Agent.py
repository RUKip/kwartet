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
        # ~ if self.id == 1:
            # ~ return self.askPossibleCards()
        # ~ elif self.id == 2:
            # ~ return self.askKnownCards()        
        return self.askKnownCardsSecondOrder()


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

    def giveCard(self, card):
        self.card_set[card.getGroup()].append(card)

    def removeCard(self, card):
        self.card_set[card.getGroup()].remove(card)

    def remove_group(self, group):
        """
        After the announcement of a kwartet, the remove_group function is 
        called. Since this is a public announcement an agent knows all 
        observers will remove the group from the model.
        """
        self.card_set[group].clear()
        for observer in self.model.players:
            self.model.group_model[group][observer][self.id] = Model.WORLD_DELETED
            for card in self.model.card_model[group][observer][self.id]:
                self.set_card_for_player(Card(group, card), observer, self.id, Model.WORLD_DELETED)

    def AnnouncementGaveCard(self, givenCard, asker_id, asked_id):
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
            self.set_card_for_player(givenCard, observer, asked_id, Model.WORLD_DELETED)
            # Check if there is still a known card
            known_cards = 0
            for card in self.model.card_model[givenCard.getGroup()][observer][asked_id]:
                if (self.model.card_model[givenCard.getGroup()][observer][asked_id][card] == Model.WORLD_KNOWN):
                    known_cards += 1
            if (known_cards == 0):
                self.set_group_for_player(givenCard, observer, asked_id, Model.WORLD_MAYBE)

            # Updating model for the player(asker_id)
            self.set_card_for_player(givenCard, observer, asker_id, Model.WORLD_KNOWN)
            self.set_group_for_player(givenCard, observer, asker_id, Model.WORLD_KNOWN)

    def AnnouncementNotCard(self, card, asker_id, asked_id):
        """
        After the announcement that player(asked_id) does not have a card,
        we update the agent's model. Everyone knows that player(asker_id) 
        has the group of the requested card. Everyone knows that 
        player(asked_id) doesn't have that card.

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
        All players know that cards belonging to that group are not possible anymore

        Args:
            group: card group

        Returns:
            Nothing

        """
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
        
        # Go through everyone's card status. If anybody has 4 Model.WORLD_DELETED, then group deleted.
        for group in self.model.card_model.keys():
            for observer in self.model.players:
                for player in self.model.players:
                    aux = sum(self.model.card_model[group][observer][player].values())
                    if aux == -4:
                        self.model.group_model[group][observer][player] = self.model.WORLD_DELETED

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
                    for player in self.model.players:
                        if self.model.card_model[group][observer][player][card] == Model.WORLD_DELETED:
                            deleted_cards += 1
                        else:
                            stored_player = player
                    if (deleted_cards == (len(self.model.players) - 1)):
                        self.model.card_model[group][observer][stored_player][card] = Model.WORLD_KNOWN
                        self.model.group_model[group][observer][stored_player] = Model.WORLD_KNOWN

    def setModel(self, model):
        self.model = model

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

    def set_card_for_player(self, card, observer, player_id, operator):
        self.model.card_model[card.getGroup()][observer][player_id][card.getCard()] = operator

    def set_group_for_player(self, card, observer, player_id, operator):
        self.model.group_model[card.getGroup()][observer][player_id] = operator

    def askPossibleCards(self):
        logging.info("Player %d will ask for a random possible card." %self.id)
        logging.info("Player card set: " + str(self.card_set))

        possible_cards = []
        for group in self.card_set:
            if self.card_set[group]:    # player is allowed to ask for a card in this group
                for player in self.opponents:
                    for card in self.model.card_model[group][self.id][player]:
                        if self.model.card_model[group][self.id][player][card] == self.model.WORLD_KNOWN:
                            possible_cards.append((Card(group, card), player))
                        if self.model.card_model[group][self.id][player][card] == self.model.WORLD_MAYBE:
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
                for card in self.model.card_model[rand_group][self.id][self.id].keys():
                    if self.model.card_model[rand_group][self.id][self.id][card] == Model.WORLD_DELETED:
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
        logging.info("Known groups: " + str(known_groups))
        logging.info("Possible groups: " + str(possible_groups))

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
        # delete player in model (to update output graph model)
        for group in self.model.group_model:
            for observer in self.model.players:
                for player in self.model.players:
                    if player == dead_player_id:
                        self.model.group_model[group][observer][player] = Model.WORLD_DELETED
                        self.model.card_model[group][observer][player] = Model.WORLD_DELETED
                        
        # delete observer in model (to update output graph model)
        for group in self.model.group_model:
            for observer in self.model.players:
                if observer == dead_player_id:
                    self.model.group_model[group][observer] = Model.WORLD_DELETED
                    self.model.card_model[group][observer] = Model.WORLD_DELETED
        
        # remove player from game

        self.model.players.remove(dead_player_id)
        if (self.id != dead_player_id):
            logging.info("Player " + str(self.id) + " opponents: " + str(self.opponents))
            logging.info("Player " + str(self.id) + " wants to remove player " + str(dead_player_id) + " from opponents.")
            self.opponents.remove(dead_player_id)
            logging.info("Player " + str(self.id) + " opponents: " + str(self.opponents))
         
        logging.info("Player " + str(self.id) + " now knows player " + str(dead_player_id) + " sleeps with the fishes. RIP")
