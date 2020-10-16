import unittest
import whist_game


class MyTestCase(unittest.TestCase):
    def test_deck_size(self):
        deck = whist_game.Deck()
        deck_size = len(deck.cards_in_deck)
        self.assertEqual(52, deck_size)

    def test_deal_cards(self):
        deck = whist_game.Deck()
        players = [whist_game.Player(),whist_game.Player(),whist_game.Player(),whist_game.Player()]
        dealer = whist_game.Dealer(deck)
        dealer.deal_cards(players)
        for p in players:
            hand_size = len(p.hand.cards_in_hand)
            self.assertEqual(13, hand_size)

    def test_play_card(self):
        deck = whist_game.Deck()
        players = [whist_game.Player(),whist_game.Player(),whist_game.Player(),whist_game.Player()]
        dealer = whist_game.Dealer(deck)
        dealer.deal_cards(players)
        for p in players:
            max_card = max(p.hand.cards_in_hand, key=lambda c: c.value)
            max_card_value = max_card.value
            card_played = p.play_card(current_winning_card=None)
            card_played_value = card_played.value
            self.assertEqual(max_card_value, card_played_value)


if __name__ == '__main__':
    unittest.main()
