import random
import copy
from abc import ABC, abstractmethod

# List for each card comprises card suit, card rank, card value.
card_list = [["Clubs", "2", 2], ["Clubs", "3", 3], ["Clubs", "4", 4], ["Clubs", "5", 5], ["Clubs", "6", 6],
             ["Clubs", "7", 7],
             ["Clubs", "8", 8], ["Clubs", "9", 9], ["Clubs", "10", 10], ["Clubs", "Jack", 11], ["Clubs", "Queen", 12],
             ["Clubs", "King", 13], ["Clubs", "Ace", 14], ["Hearts", "2", 2], ["Hearts", "3", 3], ["Hearts", "4", 4],
             ["Hearts", "5", 5], ["Hearts", "6", 6], ["Hearts", "7", 7], ["Hearts", "8", 8], ["Hearts", "9", 9],
             ["Hearts", "10", 10],
             ["Hearts", "Jack", 11], ["Hearts", "Queen", 12], ["Hearts", "King", 13], ["Hearts", "Ace", 14],
             ["Diamonds", "2", 2], ["Diamonds", "3", 3], ["Diamonds", "4", 4], ["Diamonds", "5", 5],
             ["Diamonds", "6", 6], ["Diamonds", "7", 7],
             ["Diamonds", "8", 8], ["Diamonds", "9", 9], ["Diamonds", "10", 10], ["Diamonds", "Jack", 11],
             ["Diamonds", "Queen", 12],
             ["Diamonds", "King", 13], ["Diamonds", "Ace", 14], ["Spades", "2", 2], ["Spades", "3", 3],
             ["Spades", "4", 4],
             ["Spades", "5", 5], ["Spades", "6", 6], ["Spades", "7", 7], ["Spades", "8", 8], ["Spades", "9", 9],
             ["Spades", "10", 10],
             ["Spades", "Jack", 11], ["Spades", "Queen", 12], ["Spades", "King", 13], ["Spades", "Ace", 14]]

# A game has nine rounds, there is a trump suit for each round.
trump_list = ["Hearts", "Diamonds", "Spades", "Clubs", "No Trumps", "Hearts", "Diamonds", "Spades", "Clubs"]

suit_list = ["Hearts", "Diamonds", "Spades", "Clubs"]


class Card:
    """Card class represents the cards in a deck of cards. Cards are instantiated by the Deck class."""

    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        # return 'Suit = ' + self.suit + ' Rank = ' + self.rank + ' Value = ' + str(self.value)
        return 'Suit = {}, Rank = {}, Value = {}'.format(self.suit, self.rank, self.value)


class Deck:
    """Deck class is responsible for creating a shuffled deck of 52 cards stored in a list."""

    def __init__(self):
        self.cards_in_deck = []
        for card in card_list:
            new_card = Card(card[0], card[1], card[2])
            self.cards_in_deck.append(new_card)
        random.shuffle(self.cards_in_deck)

    def remove_all_cards(self):
        self.cards_in_deck.clear()


class CardValidator:
    """CardValidator class is responsible for validating the card a Player intends to play on their turn."""

    def __init__(self):
        pass

    def check_card_number(self, card_number, cards_in_hand):
        try:
            int(card_number)
        except ValueError:
            print("A card number was not entered")
            # return CardValidationError("A card number was not entered")
            return False
        try:
            cards_in_hand[int(card_number)]
        except IndexError:
            print("Card number entered was not found in hand")
            # return CardValidationError("Card number entered was not found in hand")
            return False
        else:
            return True

    def check_card_suit(self, card, lead_card, cards_in_hand):
        if card.suit == lead_card.suit:
            return True
        else:
            for card in cards_in_hand:
                if card.suit == lead_card.suit:
                    print("Hand includes cards from lead card suit ({}). Card played must follow suit."
                          .format(lead_card.suit))
                    return False
                    # return CardValidationError("Hand includes cards from lead card suit. Card played must follow suit.")
            return True

    def check_card_in_hand(self, card, cards_in_hand):
        if card in cards_in_hand:
            return True
        else:
            print("Hand does not include the card played. Card played must be in hand.")
            return False
            # return CardValidationError("Hand does not include the card played. Card played must be in hand.")

    def is_card(self, obj):
        if isinstance(obj, Card):
            return True
        else:
            return False


# class CardValidationError(Exception):
#     """Used to raise an exception if a method in CardValidator returns False"""
#     pass


class Hand:
    """Hand class is responsible for managing a Player's hand of cards."""

    def __init__(self, player):
        self.player = player
        self.cards_in_hand = []

    def add_card(self, card):
        self.cards_in_hand.append(card)

    def remove_card(self, card):
        self.cards_in_hand.remove(card)

    def sort_cards(self):
        """Sort cards in descending order based on the card's value."""
        self.cards_in_hand.sort(key=lambda c: c.value, reverse=True)


class Player(ABC):
    """Player class represents an abstract Player class. Concrete Player subclasses inherit from this abstract class,
    and override the abstract methods.

    There are four players in a game. Player class returns the card it intends to play, selected from a Hand of cards.
    """
    def __init__(self, name, validator):
        # self.player_num = Player.playerCounter
        # Player.playerCounter += 1
        super().__init__()
        self.name = name
        self.trick_score = 0
        self.round_score = 0
        self.validator = validator

        # self.cards_in_hand = []

    # def add_card(self, card):
    #     self.cards_in_hand.append(card)
    #
    # def remove_card(self, card):
    #     self.cards_in_hand.remove(card)
    #
    # def sort_cards(self):
    #     """Sort cards in descending order based on the card's value."""
    #     self.cards_in_hand.sort(key=lambda c: c.value, reverse=True)

    @abstractmethod
    def play_lead_card(self, cards_in_hand, trump_suit):
        """ Player who leads a Trick plays the first card (the lead card).

        Implement logic to select the lead card from the cards_in_hand, and return it.
        """
        pass

    @abstractmethod
    def play_follow_card(self, cards_in_hand, trump_suit, current_winning_card, lead_card):
        """All Players other than Player who leads a Trick play a follow card.

        Players must play a card that follows suit of lead card (if available). If cards in lead suit are not available
        the Player can play any card from another suit, including the trump suit. The highest card played from the trump
        suit will win the Trick, however, in the absence of cards from the trump suit, the highest card played from the
        lead suit will win the Trick.

        Implement logic to select the follow card from the cards_in_hand, and return it.
        """
        pass

    def _check_suit_available(self, cards_in_hand, suit):
        for card in cards_in_hand:
            if card.suit == suit:
                return True
        return False

    def _find_lowest_card_in_suit(self, cards_in_hand, suit):
        cards_in_suit = []
        for card in cards_in_hand:
            if card.suit == suit:
                cards_in_suit.append(card)
        if len(cards_in_suit):
            lowest_card = cards_in_suit[0]
            for card in cards_in_suit:
                if card.value < lowest_card.value:
                    lowest_card = card
            return lowest_card

    def _find_highest_card_in_suit(self, cards_in_hand, suit):
        cards_in_suit = []
        for card in cards_in_hand:
            if card.suit == suit:
                cards_in_suit.append(card)
        if len(cards_in_suit):
            highest_card = cards_in_suit[0]
            for card in cards_in_suit:
                if card.value > highest_card.value:
                    highest_card = card
            return highest_card

    def show_hand(self, cards_in_hand):
        if len(cards_in_hand):
            # print('Displaying ' + self.name + "'s hand:")
            print("Displaying {}'s hand:".format(self.name))
            for i in range(len(cards_in_hand)):
                print(str(i) + ": " + cards_in_hand[i].__str__())
        else:
            # print(self.name + "'s hand is empty")
            print("{}'s hand is empty".format(self.name))


class ComputerPlayer(Player):
    """ComputerPlayer class represents a non-human controlled player."""
    def __init__(self, name, validator):
        # self.player_num = Player.playerCounter
        # Player.playerCounter += 1
        super().__init__(name, validator)
        # self.name = name
        # self.trick_score = 0
        # self.round_score = 0
        # self.validator = validator
        # self.cards_in_hand = []

    # def add_card(self, card):
    #     self.cards_in_hand.append(card)
    #
    # def remove_card(self, card):
    #     self.cards_in_hand.remove(card)
    #
    # def sort_cards(self):
    #     """Sort cards in descending order based on the card's value."""
    #     self.cards_in_hand.sort(key=lambda c: c.value, reverse=True)

    def play_lead_card(self, cards_in_hand, trump_suit):
        """ Player who leads a Trick plays a card in Trump suit (if available), otherwise card with highest value."""
        if self._check_suit_available(cards_in_hand, trump_suit):
            highest_card = self._find_highest_card_in_suit(cards_in_hand, trump_suit)
            # card_to_play = copy.copy(highest_card)
            # self.remove_card(highest_card)
            card_to_play = highest_card
            return card_to_play
        else:
            # card_to_play = copy.copy(self.cards_in_hand[0])
            # self.remove_card(self.cards_in_hand[0])
            card_to_play = cards_in_hand[0]
            return card_to_play

    def play_follow_card(self, cards_in_hand, trump_suit, current_winning_card, lead_card):
        """All Players other than Player who leads a Trick play a follow card.

        Players must play a card that follows suit of lead card (if available). If the highest value card in lead suit
        is higher than the current winning card, and the current winning card's suit matches the lead suit, play
        card otherwise play lowest value card in lead suit.

        If cards in lead suit not available, next check if any cards in trump suit. If current winning card is in trump
        suit,and highest value card in trump suit is higher than current winning card, play card. If current winning
        card, not in trump suit, play lowest value card in trump suit.

        If no cards available in lead suit or trump suit, find lowest value cards in two remaining suits. Sort these
        cards in ascending order and play lowest value card.
        """
        # Player must play card from lead suit (if available)
        if self._check_suit_available(cards_in_hand, lead_card["card"].suit):
            highest_card = self._find_highest_card_in_suit(cards_in_hand, lead_card["card"].suit)
            if highest_card.value > current_winning_card["card"].value and current_winning_card["card"].suit \
                    == lead_card["card"].suit:
                # card_to_play = copy.copy(highest_card)
                # self.remove_card(highest_card)
                card_to_play = highest_card
                return card_to_play
            else:
                lowest_card = self._find_lowest_card_in_suit(cards_in_hand, lead_card["card"].suit)
                # card_to_play = copy.copy(lowest_card)
                # self.remove_card(lowest_card)
                card_to_play = lowest_card
                return card_to_play

        # If lead suit card not available, check for cards in trump suit
        else:
            if self._check_suit_available(cards_in_hand, trump_suit):
                if current_winning_card["card"].suit == trump_suit:
                    highest_card = self._find_highest_card_in_suit(cards_in_hand, trump_suit)
                    if highest_card.value > current_winning_card["card"].value:
                        # card_to_play = copy.copy(highest_card)
                        # self.remove_card(highest_card)
                        card_to_play = highest_card
                        return card_to_play
                elif current_winning_card["card"].suit != trump_suit:
                    lowest_card = self._find_lowest_card_in_suit(cards_in_hand, trump_suit)
                    # card_to_play = copy.copy(lowest_card)
                    # self.remove_card(lowest_card)
                    card_to_play = lowest_card
                    return card_to_play

            # If neither lead suit or trump suit cards available, play lowest card from other suits
            else:
                other_suits = copy.copy(suit_list)
                other_suits.remove(lead_card["card"].suit)
                if trump_suit in other_suits:
                    other_suits.remove(trump_suit)
                lowest_cards = []
                for suit in other_suits:
                    if self._check_suit_available(cards_in_hand, suit):
                        lowest_cards.append(self._find_lowest_card_in_suit(cards_in_hand, suit))
                lowest_cards.sort(key=lambda c: c.value)
                lowest_card = lowest_cards[0]
                # card_to_play = copy.copy(lowest_card)
                # self.remove_card(lowest_card)
                card_to_play = lowest_card
                return card_to_play

    # def _check_suit_available(self, cards_in_hand, suit):
    #     return super()._check_suit_available(cards_in_hand, suit)
        # for card in cards_in_hand:
        #     if card.suit == suit:
        #         return True
        # return False

    # def _find_lowest_card_in_suit(self, cards_in_hand, suit):
    #     return super()._find_lowest_card_in_suit(cards_in_hand, suit)
        # cards_in_suit = []
        # for card in cards_in_hand:
        #     if card.suit == suit:
        #         cards_in_suit.append(card)
        # if len(cards_in_suit):
        #     lowest_card = cards_in_suit[0]
        #     for card in cards_in_suit:
        #         if card.value < lowest_card.value:
        #             lowest_card = card
        #     return lowest_card

    # def _find_highest_card_in_suit(self, cards_in_hand, suit):
    #     return super()._find_highest_card_in_suit(cards_in_hand, suit)
        # cards_in_suit = []
        # for card in cards_in_hand:
        #     if card.suit == suit:
        #         cards_in_suit.append(card)
        # if len(cards_in_suit):
        #     highest_card = cards_in_suit[0]
        #     for card in cards_in_suit:
        #         if card.value > highest_card.value:
        #             highest_card = card
        #     return highest_card

    # def show_hand(self, cards_in_hand):
    #     return super().show_hand(cards_in_hand)
        # if len(cards_in_hand):
        #     # print('Displaying ' + self.name + "'s hand:")
        #     print("Displaying {}'s hand:".format(self.name))
        #     for i in range(len(cards_in_hand)):
        #         print(str(i) + ": " + cards_in_hand[i].__str__())
        # else:
        #     # print(self.name + "'s hand is empty")
        #     print("{}'s hand is empty".format(self.name))


class HumanPlayer(Player):
    def __init__(self, name, validator):
        super().__init__(name, validator)
        # self.trick_score = 0
        # self.round_score = 0

    def play_lead_card(self, cards_in_hand, trump_suit):
        self.show_hand(cards_in_hand)
        card_number_str, card = None, None
        is_valid = False
        while not is_valid:
            card_number_str = input("Please select a card to start the trick by entering the card number: ")
            if not self.validator.check_card_number(card_number_str, cards_in_hand):
                continue
            card = cards_in_hand[int(card_number_str)]
            if not self.validator.check_card_in_hand(card, cards_in_hand):
                continue
            is_valid = True
        # card_to_play = copy.copy(card)
        # self.remove_card(card)
        card_to_play = card
        return card_to_play
        # try:
        #     card_number = int(input("Please select a card to start the trick by entering the card number: "))
        #     if card_number not in range(len(self.cards_in_hand)):
        #         raise IndexError
        # except ValueError:
        #     print("A card number was not entered")
        # except IndexError:
        #     print("Card number entered was not found in hand")
        # else:
        #     card = self.cards_in_hand[card_number]
        #     card_to_play = copy.copy(card)
        #     self.remove_card(card)
        #     return card_to_play

    def play_follow_card(self, cards_in_hand, trump_suit, current_winning_card, lead_card):
        self.show_hand(cards_in_hand)
        # print("The leading card is: " + lead_card["card"].__str__() + " played by:"
        # + lead_card["player"].name)
        print("The leading card is: {} played by: {}".format(lead_card["card"].__str__(), lead_card["player"].name))
        # print("The current winning card is: " + current_winning_card["card"].__str__() + " played by:"
        #       + current_winning_card["player"].name)
        print("The current winning card is: {} played by: {}".format(current_winning_card["card"].__str__(),
                                                                     current_winning_card["player"].name))
        card_number_str, card = None, None
        is_valid = False
        while not is_valid:
            card_number_str = input("Please select a card to play by entering the card number: ")
            if not self.validator.check_card_number(card_number_str, cards_in_hand):
                continue
            card = cards_in_hand[int(card_number_str)]
            if not self.validator.check_card_suit(card, lead_card["card"], cards_in_hand):
                continue
            if not self.validator.check_card_in_hand(card, cards_in_hand):
                continue
            is_valid = True
        # card_number_str = input("Please select a card to play by entering the card number: ")
        # while not self.validator.check_card_number(card_number_str, cards_in_hand):
        #     card_number_str = input("Please select a card to play by entering the card number: ")
        # card = cards_in_hand[int(card_number_str)]
        # card_to_play = copy.copy(card)
        # self.remove_card(card)
        card_to_play = card
        return card_to_play

    # def _validate_card_number(self, card_number, cards_in_hand):
    #     try:
    #         int(card_number)
    #     except ValueError:
    #         print("A card number was not entered")
    #         return False
    #     try:
    #         cards_in_hand[int(card_number)]
    #     except IndexError:
    #         print("Card number entered was not found in hand")
    #         return False
    #     else:
    #         return True

    # def _validate_card_suit(self, card_suit, lead_card_suit):
    #     try:
    #         int(card_number)
    #     except ValueError:
    #         print("A card number was not entered")
    #         return False
    #     try:
    #         self.cards_in_hand[int(card_number)]
    #     except IndexError:
    #         print("Card number entered was not found in hand")
    #         return False
    #     else:
    #         return True


# TODO - implement PlayerTeam class

# class PlayerTeam:
#     def __init__(self, member1, member2):
#         self.member1 = member1
#         self.member2 = member2
#         self.points = 0
#
#     def add_point(self):
#         self.points +=1


class Dealer:
    """Dealer class represents a card dealer. There is one dealer per game."""

    def __init__(self, deck):
        self.deck = deck

    def deal_cards(self, hands):
        """Deal a deck of cards to the player's hands.

         Deal cards by adding a card to each player's hand, one at a time in the order of the players list.
         """
        cards_dealt = 0
        next_hand = 0
        for card in self.deck.cards_in_deck:
            hands[next_hand].add_card(card)
            next_hand += 1
            next_hand = next_hand % 4
            cards_dealt += 1
        self.deck.remove_all_cards()
        # print("Dealt: " + str(cards_dealt) + " cards.")
        print("Dealt: {} cards.".format(str(cards_dealt)))


class Trick:
    """A Trick represents one turn, where each player plays one card. There are 13 tricks in 1 round."""

    def __init__(self, players, hands, trump_suit, validator):
        self.players = players
        self.hands = hands
        self.trump_suit = trump_suit
        self.current_winning_card = None
        self.cards_played_dicts = []
        self.winning_player = None
        self.validator = validator

    def _update_current_winning_card(self):
        """Set the current winning card for the Trick.

         If the lead suit is the trump suit, cards only need to be split by trump suit or other suits. However,
         if lead suit is not trump suit, cards are split by lead suit, trump suit, or other suits. If the trump
         suit list has any cards, return the card with the highest value. Otherwise, return the card with the
         highest value from the lead suit list.
         """
        lead_suit_cards = []
        trump_suit_cards = []
        other_suit_cards = []
        for card in self.cards_played_dicts:
            if self.cards_played_dicts[0]["card"].suit == self.trump_suit:
                if card["card"].suit == self.trump_suit:
                    trump_suit_cards.append(card)
                else:
                    other_suit_cards.append(card)
            else:
                if card["card"].suit == self.cards_played_dicts[0]["card"].suit:
                    lead_suit_cards.append(card)
                elif card["card"].suit == self.trump_suit:
                    trump_suit_cards.append(card)
                else:
                    other_suit_cards.append(card)
        if len(trump_suit_cards):
            trump_suit_cards.sort(key=lambda c: c["card"].value, reverse=True)
            self.current_winning_card = trump_suit_cards[0]
        else:
            lead_suit_cards.sort(key=lambda c: c["card"].value, reverse=True)
            self.current_winning_card = lead_suit_cards[0]

    def play_trick(self):
        """Each player plays one card. First player plays a lead card, other players play follow cards.

         The first player is the previous Trick's winner, or if first Trick it is the first Player instantiated.
         """
        for player in self.players:
            hand = next(filter(lambda h: h.player is player, self.hands))
            card = None
            if player is self.players[0]:
                is_valid = False
                while not is_valid:
                    card = player.play_lead_card(hand.cards_in_hand, self.trump_suit)
                    if not self.validator.is_card(card):
                        continue
                    if not self.validator.check_card_in_hand(card, hand.cards_in_hand):
                        continue
                    is_valid = True
            else:
                is_valid = False
                while not is_valid:
                    card = player.play_follow_card(hand.cards_in_hand, self.trump_suit, self.current_winning_card,
                                               self.cards_played_dicts[0])
                    if not self.validator.is_card(card):
                        continue
                    if not self.validator.check_card_suit(card, self.cards_played_dicts[0]["card"], hand.cards_in_hand):
                        continue
                    if not self.validator.check_card_in_hand(card, hand.cards_in_hand):
                        continue
                    is_valid = True
            card_played = copy.copy(card)
            hand.remove_card(card)
            card_played_dict = {"player": player, "card": card_played}
            self.cards_played_dicts.append(card_played_dict)
            self._update_current_winning_card()
        self.winning_player = self.current_winning_card["player"]
        self.winning_player.trick_score += 1
        self._show_trick_result()
        for player in self.players:
            hand = next(filter(lambda h: h.player is player, self.hands))
            player.show_hand(hand.cards_in_hand)

    def _show_trick_result(self):
        print("---Cards played in Trick---")
        for card in self.cards_played_dicts:
            # print(card["player"].name + " played: " + card["card"].__str__())
            print("{} played: {}".format(card["player"].name, card["card"].__str__()))
        print("-- Winning card---")
        # print(self.current_winning_card["player"].name + " played: " + self.current_winning_card["card"].__str__())
        print("{} played: {}".format(self.current_winning_card["player"].name,
                                     self.current_winning_card["card"].__str__()))


class Round:
    """A Round comprises 13 tricks. The player (or players if there is a tie) who win the most tricks, win the round."""
    TRICKS_PER_ROUND = 13

    def __init__(self, players, hands, trump_suit, validator):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.players = players
        self.hands = hands
        self.trump_suit = trump_suit
        self.trick_number = 0
        self.last_trick_winner = None
        self.winning_players = []
        self.validator = validator

    def play_round(self):
        self.dealer.deal_cards(self.hands)
        for hand in self.hands:
            hand.sort_cards()
        for _ in range(self.TRICKS_PER_ROUND):
            trick = Trick(self._sort_players(self.players), self.hands, self.trump_suit, self.validator)
            trick.play_trick()
            self.last_trick_winner = trick.winning_player
            self.trick_number += 1
        self._score_round()

    def _get_starting_player_index(self):
        """Returns player who will start the next Trick"""
        if self.trick_number == 0:
            return 0
        else:
            return self.players.index(self.last_trick_winner)

    def _get_next_player_index(self, current_player_index):
        return (current_player_index + 1) % 4

    def _sort_players(self, players):
        sorted_players = []
        player_index = self._get_starting_player_index()
        for _ in range(len(players)):
            sorted_players.append(players[player_index])
            player_index = self._get_next_player_index(player_index)
        return sorted_players

    def _score_round(self):
        trick_scores = []
        for player in self.players:
            trick_scores.append(player.trick_score)
        highest_trick_score = max(trick_scores)
        for player in self.players:
            if player.trick_score == highest_trick_score:
                player.round_score += 1
                self.winning_players.append(player)
        if len(self.winning_players) > 1:
            # for player in self.winning_players:
                # print(player.name + " tied the round with " + str(player.trick_score) + " wins.")
            print("{} tied the round with {} wins.".format(", ".join(self.winning_players), str(highest_trick_score)))
        else:
            # print(self.winning_players[0].name + " won the round with " + str(self.winning_players[0].trick_score)
            #       + " wins.")
            print("{} won the round with {} wins.".format(self.winning_players[0].name,
                                                          self.winning_players[0].trick_score))


# TODO: A Game currently comprises 1 round. Game class will be updated to change to max 13, where first player to win
#  4 rounds wins the game.

class Game:
    def __init__(self):
        self.validator = CardValidator()
        self.players = []
        self.players.append(HumanPlayer(input("Please enter your name: "), self.validator))
        computer_player_names = ["Tee", "Sam", "Cat"]
        for cp in computer_player_names:
            self.players.append(ComputerPlayer(cp, self.validator))
        self.hands = []
        for player in self.players:
            self.hands.append(Hand(player))
        self.round_num = 0

    def play_game(self):
        trump_suit = trump_list[self.round_num]
        round_ = Round(self.players, self.hands, trump_suit, self.validator)
        # print("---Playing Round " + str(self.round_num) + "---")
        # print("Trump suit is: " + trump_suit)
        print("---Playing Round {}---".format(str(self.round_num)))
        print("Trump suit is: {}".format(trump_suit))
        round_.play_round()


def main():
    game = Game()
    game.play_game()


if __name__ == "__main__":
    main()
