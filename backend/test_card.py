from app.game.card import Card, Suit, Rank
from app.game.deck import Deck
from app.game.hand import Hand

# 測試 Hand
print("=== 測試 Hand ===\n")

# 情況 1: 普通手牌
hand1 = Hand()
hand1.add_card(Card(Suit.HEARTS, Rank.KING))   # K♥ = 10
hand1.add_card(Card(Suit.SPADES, Rank.SEVEN))  # 7♠ = 7
print(f"手牌 1: {hand1}")
print(f"所有可能值: {hand1.get_values()}")
print(f"最佳值: {hand1.get_best_value()}")
print(f"是否爆牌: {hand1.is_bust()}")
print()

# 情況 2: Blackjack
hand2 = Hand()
hand2.add_card(Card(Suit.CLUBS, Rank.ACE))     # A♣ = 1 or 11
hand2.add_card(Card(Suit.DIAMONDS, Rank.KING)) # K♦ = 10
print(f"手牌 2: {hand2}")
print(f"所有可能值: {hand2.get_values()}")
print(f"是否 Blackjack: {hand2.is_blackjack()}")
print()

# 情況 3: 爆牌
hand3 = Hand()
hand3.add_card(Card(Suit.HEARTS, Rank.KING))   # K♥ = 10
hand3.add_card(Card(Suit.SPADES, Rank.QUEEN))  # Q♠ = 10
hand3.add_card(Card(Suit.DIAMONDS, Rank.FIVE)) # 5♦ = 5
print(f"手牌 3: {hand3}")
print(f"所有可能值: {hand3.get_values()}")
print(f"是否爆牌: {hand3.is_bust()}")
print()

# 情況 4: 多個 A
hand4 = Hand()
hand4.add_card(Card(Suit.HEARTS, Rank.ACE))    # A♥
hand4.add_card(Card(Suit.SPADES, Rank.ACE))    # A♠
hand4.add_card(Card(Suit.DIAMONDS, Rank.NINE)) # 9♦
print(f"手牌 4: {hand4}")
print(f"所有可能值: {hand4.get_values()}")
print(f"最佳值: {hand4.get_best_value()}")