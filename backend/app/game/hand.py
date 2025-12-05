from typing import List
from .card import Card


class Hand:
    """一手牌（玩家或莊家持有的牌）"""
    
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card) -> None:
        """加一張牌到手中"""
        self.cards.append(card)
    
    def get_values(self) -> List[int]:
        """
        計算手牌所有可能的點數總和
        例如：A + 5 → [6, 16]（1+5 或 11+5）
        """
        if not self.cards:
            return [0]
        
        # 從第一張牌開始計算
        possible_values = self.cards[0].get_values()
        
        # 逐張加入其他牌，計算所有可能的組合
        for card in self.cards[1:]:
            card_values = card.get_values()
            new_possible_values = []
            
            for total in possible_values:
                for value in card_values:
                    new_possible_values.append(total + value)
            
            possible_values = new_possible_values
        
        # 移除重複值並排序
        return sorted(list(set(possible_values)))
    
    def get_best_value(self) -> int:
        """
        取得最佳點數（盡量接近 21 但不超過）
        如果全部都超過 21，回傳最小的值
        """
        values = self.get_values()
        
        # 找出所有 <= 21 的值
        valid_values = [v for v in values if v <= 21]
        
        if valid_values:
            return max(valid_values)  # 回傳最接近 21 的值
        else:
            return min(values)  # 全部爆牌，回傳最小值
    
    def is_bust(self) -> bool:
        """判斷是否爆牌（所有可能值都 > 21）"""
        return all(v > 21 for v in self.get_values())
    
    def is_blackjack(self) -> bool:
        """判斷是否為 Blackjack（兩張牌共 21 點）"""
        return len(self.cards) == 2 and 21 in self.get_values()
    
    def clear(self) -> None:
        """清空手牌"""
        self.cards = []
    
    def __str__(self) -> str:
        cards_str = ", ".join(str(card) for card in self.cards)
        return f"[{cards_str}] = {self.get_best_value()}"
    
    def __repr__(self) -> str:
        return self.__str__()