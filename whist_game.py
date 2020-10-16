import random
import copy

card_list = [["Clubs", "2", 2], ["Clubs", "3", 3], ["Clubs", "4", 4], ["Clubs", "5", 5], ["Clubs", "6", 6], ["Clubs", "7", 7],
             ["Clubs", "8", 8], ["Clubs", "9", 9], ["Clubs", "10", 10], ["Clubs", "Jack", 11], ["Clubs", "Queen", 12],
             ["Clubs", "King", 13], ["Clubs", "Ace", 14], ["Hearts", "2", 2], ["Hearts", "3", 3], ["Hearts", "4", 4],
             ["Hearts", "5", 5], ["Hearts", "6", 6], ["Hearts", "7", 7], ["Hearts", "8", 8], ["Hearts", "9", 9], ["Hearts", "10", 10],
             ["Hearts", "Jack", 11], ["Hearts", "Queen", 12], ["Hearts", "King", 13], ["Hearts", "Ace", 14],
             ["Diamonds", "2", 2], ["Diamonds", "3", 3], ["Diamonds", "4", 4], ["Diamonds", "5", 5], ["Diamonds", "6", 6], ["Diamonds", "7", 7],
             ["Diamonds", "8", 8], ["Diamonds", "9", 9], ["Diamonds", "10", 10], ["Diamonds", "Jack", 11], ["Diamonds", "Queen", 12],
             ["Diamonds", "King", 13], ["Diamonds", "Ace", 14], ["Spades", "2", 2], ["Spades", "3", 3], ["Spades", "4", 4],
             ["Spades", "5", 5], ["Spades", "6", 6], ["Spades", "7", 7], ["Spades", "8", 8], ["Spades", "9", 9], ["Spades", "10", 10],
             ["Spades", "Jack", 11], ["Spades", "Queen", 12],["Spades", "King", 13], ["Spades", "Ace", 14]]

trump_list = ["Hearts", "Diamonds", "Spades", "Clubs", "No Trumps", "Hearts", "Diamonds", "Spades", "Clubs"]

suit_list = ["Hearts", "Diamonds", "Spades", "Clubs"]


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value


class Deck:
    def __init__(self):
        self.cards_in_deck = []
        for card in card_list:
            new_card = Card(card[0],card[1],card[2])
            self.cards_in_deck.append(new_card)
        random.shuffle(self.cards_in_deck)

    def remove_all_cards(self):
        self.cards_in_deck.clear()

# remove Hand class, add cards in hand list and methods under player class

# class Hand:
#     def __init__(self):
#         self.cards_in_hand = []
# 
#     def add_card(self, card):
#         self.cards_in_hand.append(card)
# 
#     def remove_card(self, card):
#         self.cards_in_hand.remove(card)


class Player:
    playerCounter = 0

    def __init__(self, name):
        self.player_num = Player.playerCounter
        Player.playerCounter += 1
        self.name = name
        self.cards_in_hand = []
        
    def add_card(self, card):
        self.cards_in_hand.append(card)

    def remove_card(self, card):
        self.cards_in_hand.remove(card)

    def sort_cards(self):
        self.cards_in_hand.sort(key=lambda c: c.value, reverse=True)

    def play_lead_card(self, trump_suit):
        for card in self.cards_in_hand:
            if card.suit == trump_suit:
                print("lead contains trump cards")
                card_to_play = copy.copy(card)
                self.remove_card(card)
                return card_to_play
        else:
            card_to_play = copy.copy(self.cards_in_hand[0])
            self.remove_card(self.cards_in_hand[0])
            return card_to_play

    def play_follow_card(self, trump_suit, current_winning_card, lead_card):
        if self.check_suit_available(self.cards_in_hand, lead_card["card"].suit):
            print("follow contains lead cards")
            highest_card = self.find_highest_card_in_suit(self.cards_in_hand, lead_card["card"].suit)
        # if highest_card is not None:
            if highest_card.value > current_winning_card["card"].value and current_winning_card["card"].suit \
                    == lead_card["card"].suit:
                card_to_play = copy.copy(highest_card)
                self.remove_card(highest_card)
                return card_to_play
            else:
                lowest_card = self.find_lowest_card_in_suit(self.cards_in_hand, lead_card["card"].suit)
                card_to_play = copy.copy(lowest_card)
                self.remove_card(lowest_card)
                return card_to_play

        else:
            if self.check_suit_available(self.cards_in_hand, trump_suit):
                print("contains trump cards")
                if current_winning_card["card"].suit == trump_suit:
                    highest_card = self.find_highest_card_in_suit(self.cards_in_hand, trump_suit)
                    if highest_card.value > current_winning_card["card"].value:
                        card_to_play = copy.copy(highest_card)
                        self.remove_card(highest_card)
                        return card_to_play
                elif current_winning_card["card"].suit != trump_suit:
                    lowest_card = self.find_lowest_card_in_suit(self.cards_in_hand, trump_suit)
                    card_to_play = copy.copy(lowest_card)
                    self.remove_card(lowest_card)
                    return card_to_play
            else:
                other_suits = copy.copy(suit_list)
                other_suits.remove(lead_card["card"].suit)
                if trump_suit in other_suits:
                    other_suits.remove(trump_suit)
                lowest_cards = []
                for suit in other_suits:
                    if self.check_suit_available(self.cards_in_hand, suit):
                        lowest_cards.append(self.find_lowest_card_in_suit(self.cards_in_hand, suit))
                lowest_cards.sort(key=lambda c: c.value)
                # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!reached!!!!!!!")
                # for card in lowest_cards:
                #     print(card.value)
                # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!reached!!!!!!!")
                lowest_card = lowest_cards[0]
                print("lowerst card returned----------------------------------------------" + str(lowest_card.value))
                card_to_play = copy.copy(lowest_card)
                self.remove_card(lowest_card)
                return card_to_play


            # highest card in suit is none, so find highest trump, use it if beat current winning card, or use lowest instead
            # how to check if current win card is not same suit as lead card? if no trump card either, use lowest card remaining

    def check_suit_available(self, cards, suit):
        for card in cards:
            if card.suit == suit:
                return True
        return False

    def find_lowest_card_in_suit(self, cards, suit):
        print("lowest method")
        cards_in_suit = []
        for card in cards:
            if card.suit == suit:
                cards_in_suit.append(card)
        if len(cards_in_suit):
            lowest_card = cards_in_suit[0]
            for card in cards_in_suit:
                if card.value < lowest_card.value:
                    lowest_card = card
            return lowest_card
        # else:
        #     return None

    def find_highest_card_in_suit(self, cards, suit):
        print("highest method")
        cards_in_suit = []
        for card in cards:
            if card.suit == suit:
                cards_in_suit.append(card)
        if len(cards_in_suit):
            highest_card = cards_in_suit[0]
            for card in cards_in_suit:
                if card.value > highest_card.value:
                    highest_card = card
            return highest_card
        # else:
        #     return None

    def show_hand(self):
        for card in self.cards_in_hand:
            print(card.suit + " " + str(card.value) + " " + card.rank + " " + self.name)

# class ComputerPlayer:
#     def __init__(self, hand, partner):
#         super().__init__(hand)
#         self.partner = partner
#     # def play_card(self):
#
#
# class HumanPlayer:
#     def __init__(self, hand, partner):
#         super().__init__(hand)
#         self.partner =  partner
#     # def play_card(self):

#
# class PlayerTeam:
#     def __init__(self, member1, member2):
#         self.member1 = member1
#         self.member2 = member2
#         self.points = 0
#
#     def add_point(self):
#         self.points +=1
#
#     def get_partner(self, player):
#         if player is self.member1:
#             return self.member2
#         else: return self.member1


class Dealer:
    def __init__(self, deck):
        self.deck = deck

    def deal_cards(self, players):
        print("deal_cards_called")
        cards_dealt = 0
        next_player = 0
        for card in self.deck.cards_in_deck:
            players[next_player].add_card(card)
            # if next_player == 3:
            next_player += 1
            next_player = next_player % 4
            cards_dealt += 1
        self.deck.remove_all_cards()
        print("-----------------dealt " + str(cards_dealt))


class Trick:
    def __init__(self, players, trump_suit):
        self.players = players
        self.trump_suit = trump_suit
        self.current_winning_card = None
        # self.lead_card = None
        # self.second_card = None
        # self.third_card = None
        # self.fourth_card = None
        self.cards_played = []
        self.winner = None

    # @property
    # def winner(self):
    #     return self.winner

    def find_current_winning_card(self, cards_played):
        lead_suit_cards = []
        trump_suit_cards = []
        other_suit_cards = []
        for card in cards_played:
            if self.cards_played[0]["card"].suit == self.trump_suit:
                if card["card"].suit == self.trump_suit:
                    trump_suit_cards.append(card)
                else:
                    other_suit_cards.append(card)
            else:
                if card["card"].suit == self.cards_played[0]["card"].suit:
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
        self.cards_played = []
        for player in self.players:
            if player is self.players[0]:
                card = player.play_lead_card(self.trump_suit)
            else:
                card = player.play_follow_card(self.trump_suit, self.current_winning_card, self.cards_played[0])
            card_dict = {"player": player, "card": card}
            self.cards_played.append(card_dict)
            self.find_current_winning_card(self.cards_played)
        self.winner = self.current_winning_card["player"]


        # cards_played = []
        # self.lead_card = {"player": self.players[self.starting_player_index], "card": self.players
        #     [self.starting_player_index].play_lead_card(self.trump_suit)}
        # cards_played.append(self.lead_card)
        # self.find_current_winning_card(cards_played)
        # self.next_player_index = self.starting_player_index + 1
        # self.second_card = {"player": self.players[self.next_player_index], "card": self.players[self.next_player_index]
        #     .play_follow_card(self.trump_suit, self.current_winning_card, self.lead_card)}
        # cards_played.append(self.second_card)
        # self.find_current_winning_card(cards_played)
        # self.next_player_index += 1
        # self.third_card = {"player": self.players[self.next_player_index], "card": self.players[self.next_player_index]
        #     .play_follow_card(self.trump_suit, self.current_winning_card, self.lead_card)}
        # cards_played.append(self.third_card)
        # self.find_current_winning_card(cards_played)
        # self.next_player_index += 1
        # self.fourth_card = {"player": self.players[self.next_player_index], "card": self.players[self.next_player_index]
        #     .play_follow_card(self.trump_suit, self.current_winning_card, self.lead_card)}
        # cards_played.append(self.fourth_card)
        # self.find_current_winning_card(cards_played)

        # self.current_winning_card = self.lead_card
        # self.next_player_index = self.starting_player_index + 1
        # print(str(self.next_player_index))
        #
        # self.second_card = {"player": self.players[self.next_player_index], "card": self.players[self.next_player_index]
        #     .play_follow_card(self.trump_suit, self.current_winning_card, self.lead_card)}
        # if self.second_card["card"].suit == self.lead_card["card"].suit and self.second_card["card"].value > \
        #         self.lead_card["card"].value:
        #     self.current_winning_card["card"] = self.second_card["card"]
        # elif self.second_card["card"].suit == self.trump_suit:
        #     self.current_winning_card = self.second_card
        # self.next_player_index += 1
        # print(str(self.next_player_index))
        #
        # self.third_card = {"player": self.players[self.next_player_index], "card": self.players[self.next_player_index]
        #     .play_follow_card(self.trump_suit, self.current_winning_card, self.lead_card)}
        # if self.third_card["card"].suit == self.lead_card["card"].suit and self.current_winning_card["card"].suit == \
        #         self.lead_card["card"].suit:
        #     if self.third_card["card"].value > self.current_winning_card["card"].value:
        #         self.current_winning_card = self.third_card
        # elif self.third_card["card"].suit == self.trump_suit and self.current_winning_card["card"].suit \
        #         == self.trump_suit:
        #     if self.third_card["card"].value > self.current_winning_card["card"].value:
        #         self.current_winning_card = self.third_card
        # elif self.third_card["card"].suit == self.trump_suit and self.current_winning_card["card"].suit \
        #         != self.trump_suit:
        #     self.current_winning_card = self.third_card
        # self.next_player_index += 1
        # print(str(self.next_player_index))
        #
        # self.fourth_card = {"player": self.players[self.next_player_index], "card": self.players[self.next_player_index]
        #     .play_follow_card(self.trump_suit, self.current_winning_card, self.lead_card)}
        # if self.fourth_card["card"].suit == self.lead_card["card"].suit and self.current_winning_card["card"].suit \
        #         == self.lead_card["card"].suit:
        #     if self.fourth_card["card"].value > self.current_winning_card["card"].value:
        #         self.current_winning_card = self.fourth_card
        # elif self.fourth_card["card"].suit == self.trump_suit and self.current_winning_card["card"].suit \
        #         == self.trump_suit:
        #     if self.fourth_card["card"].value > self.current_winning_card["card"].value:
        #         self.current_winning_card = self.fourth_card
        # elif self.fourth_card["card"].suit == self.trump_suit and self.current_winning_card["card"].suit \
        #         != self.trump_suit:
        #     self.current_winning_card = self.fourth_card

        # print(self.current_winning_card["card"].suit + " " + str(self.current_winning_card["card"].value) + " " +
        #       self.current_winning_card["card"].rank + " " + self.current_winning_card["player"].name)
        # print(self.lead_card["card"].suit + " " + str(self.lead_card["card"].value) + " " +
        #       self.lead_card["card"].rank + " " + self.lead_card["player"].name)
        # print(self.second_card["card"].suit + " " + str(self.second_card["card"].value) + " " +
        #       self.second_card["card"].rank + " " + self.second_card["player"].name)
        # print(self.third_card["card"].suit + " " + str(self.third_card["card"].value) + " " +
        #       self.third_card["card"].rank + " " + self.third_card["player"].name)
        # print(self.fourth_card["card"].suit + " " + str(self.fourth_card["card"].value) + " " +
        #       self.fourth_card["card"].rank + " " + self.fourth_card["player"].name)

        for card in self.cards_played:
            print(card["card"].suit + " " + str(card["card"].value) + " " +
                card["card"].rank + " " + card["player"].name)
        print("----------winning card--------")
        print(self.current_winning_card["card"].suit + " " + str(self.current_winning_card["card"].value) + " " +
                    self.current_winning_card["card"].rank + " " + self.current_winning_card["player"].name)
        print("----------cards in hand--------")
        for player in self.players:
            player.show_hand()

class Round:
    TRICKS_PER_ROUND = 13

    def __init__(self, players, trump_suit):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.players = players
        self.trump_suit = trump_suit
        self.trick_number = 0
        self.last_trick_winner = None

    def play_round(self):
        self.dealer.deal_cards(self.players)
        for player in self.players:
            player.sort_cards()
        for _ in range(self.TRICKS_PER_ROUND):
            trick = Trick(self.sort_players(self.players), self.trump_suit)
            trick.play_trick()
            print("play tricky called----------------------!")
            self.last_trick_winner = trick.winner
            self.trick_number = + 1

    def get_starting_player_index(self):
        if self.trick_number == 0:
            return 0
        else: return self.players.index(self.last_trick_winner)

    def get_next_player_index(self, current_player_index):
        return (current_player_index + 1) % 4

    def sort_players(self, players):
        sorted_players = []
        player_index = self.get_starting_player_index()
        for _ in range(len(players)):
            sorted_players.append(players[player_index])
            player_index = self.get_next_player_index(player_index)
        return sorted_players





class Game:
    def __init__(self):
        self.players = [Player("Add"), Player("TDB"), Player("Sam"), Player("Cat")]
        self.round_num = 0

    def play_game(self):
        round = Round(self.players, trump_list[self.round_num])
        round.play_round()

        #end of round, shuffle index 0 player to end

    # def play_game(self):
    #     create_teams()

def main():
    game = Game()
    game.play_game()
    # dealer = Dealer(deck, players)
    # dealer.deal_cards()


if __name__ == "__main__":
    main()