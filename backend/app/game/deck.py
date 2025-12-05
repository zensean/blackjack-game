import random
from .card import Card, Suit, Rank


class Deck:
    """一副撲克牌（52張）"""
    
    def __init__(self):
        """初始化一副牌並洗牌"""
        self.cards: list[Card] = []
        self._initialize_deck()
        self.shuffle()
    
    def _initialize_deck(self) -> None:
        """建立 52 張牌（4 種花色 × 13 種點數）"""
        self.cards = [
            Card(suit, rank)
            for suit in Suit
            for rank in Rank
        ]
    
    def shuffle(self) -> None:
        """洗牌"""
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        """
        發一張牌
        
        Raises:
            IndexError: 如果牌堆空了
        """
        if len(self.cards) == 0:
            raise IndexError("牌堆已空，無法發牌")
        return self.cards.pop()
    
    def remaining_cards(self) -> int:
        """回傳剩餘牌數"""
        return len(self.cards)
    
    def __str__(self) -> str:
        return f"Deck(剩餘 {self.remaining_cards()} 張牌)"
    
    def __repr__(self) -> str:
        return self.__str__()