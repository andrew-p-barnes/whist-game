import unittest
import whist_game
import copy


class MyTestCase(unittest.TestCase):
    def test_deck_size(self):
        deck = whist_game.Deck()
        deck_size = len(deck.cards_in_deck)
        self.assertEqual(deck_size, 52)

    def test_deal_cards(self):
        deck = whist_game.Deck()
        validator = whist_game.CardValidator()
        hands = []
        players = [whist_game.HumanPlayer("p1", validator),whist_game.ComputerPlayer("p2", validator),
                   whist_game.ComputerPlayer("p3", validator),whist_game.ComputerPlayer("p4", validator)]
        for player in players:
            hands.append(whist_game.Hand(player))
        dealer = whist_game.Dealer(deck)
        dealer.deal_cards(hands)
        for hand in hands:
            hand_size = len(hand.cards_in_hand)
            self.assertEqual(hand_size, 13)

    def test_dealt_cards_unique(self):
        deck = whist_game.Deck()
        validator = whist_game.CardValidator()
        hands = []
        players = [whist_game.HumanPlayer("p1", validator),whist_game.ComputerPlayer("p2", validator),
                   whist_game.ComputerPlayer("p3", validator),whist_game.ComputerPlayer("p4", validator)]
        for player in players:
            hands.append(whist_game.Hand(player))
        dealer = whist_game.Dealer(deck)
        dealer.deal_cards(hands)
        reconstructed_deck = []
        for hand in hands:
            for card in hand.cards_in_hand:
                reconstructed_deck.append(card)
        is_unique = False
        if len(reconstructed_deck) == len(set(reconstructed_deck)):
            is_unique = True
        self.assertTrue(is_unique)

    def test_played_cards_removed(self):
        validator = whist_game.CardValidator()
        hands = []
        players = [whist_game.ComputerPlayer("p1", validator),whist_game.ComputerPlayer("p2", validator),
                   whist_game.ComputerPlayer("p3", validator),whist_game.ComputerPlayer("p4", validator)]
        for player in players:
            hands.append(whist_game.Hand(player))
        copy_of_hands = []
        for hand in hands:
            copy_of_hands.append(copy.copy(hand))
        trick = whist_game.Trick(players, hands, whist_game.trump_list[0], validator)
        trick.play_trick()
        in_hand_before_trick = True
        in_hand_after_trick = False
        for card_dict in trick.cards_played_dicts:
            player = card_dict["player"]
            copy_of_hand = next(filter(lambda h: h.player is player, copy_of_hands))
            if card_dict["card"] not in copy_of_hand:
                in_hand_before_trick = False



    # def test_play_card(self):
    #     deck = whist_game.Deck()
    #     players = [whist_game.Player(),whist_game.Player(),whist_game.Player(),whist_game.Player()]
    #     dealer = whist_game.Dealer(deck)
    #     dealer.deal_cards(players)
    #     for p in players:
    #         max_card = max(p.hand.cards_in_hand, key=lambda c: c.value)
    #         max_card_value = max_card.value
    #         card_played = p.play_card(current_winning_card=None)
    #         card_played_value = card_played.value
    #         self.assertEqual(max_card_value, card_played_value)


if __name__ == '__main__':
    unittest.main()
