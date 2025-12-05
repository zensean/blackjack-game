import pytest
from app.game.card import Card, Suit, Rank
from app.game.hand import Hand
from app.game.game import Game


class TestHand:
    """測試 Hand 類別"""
    
    def test_blackjack(self):
        """測試 Blackjack 判定"""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.KING))
        
        assert hand.is_blackjack() == True
        assert hand.get_best_value() == 21
    
    def test_bust(self):
        """測試爆牌判定"""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.KING))
        hand.add_card(Card(Suit.SPADES, Rank.QUEEN))
        hand.add_card(Card(Suit.DIAMONDS, Rank.FIVE))
        
        assert hand.is_bust() == True
        assert hand.get_best_value() == 25
    
    def test_soft_hand(self):
        """測試軟牌（有 A）"""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.SPADES, Rank.SIX))
        
        # A + 6 = 7 or 17
        assert 7 in hand.get_values()
        assert 17 in hand.get_values()
        assert hand.get_best_value() == 17


class TestGame:
    """測試 Game 類別"""
    
    def test_start_game(self):
        """測試遊戲開始"""
        game = Game()
        game.start_new_game()
        
        # 檢查發牌
        assert len(game.player_hand.cards) == 2
        assert len(game.dealer_hand.cards) == 2
    
    def test_player_hit(self):
        """測試玩家加牌"""
        game = Game()
        game.start_new_game()
        
        initial_cards = len(game.player_hand.cards)
        game.player_hit()
        
        assert len(game.player_hand.cards) == initial_cards + 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])