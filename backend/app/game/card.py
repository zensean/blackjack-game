from enum import Enum
from dataclasses import dataclass
from typing import List


class Suit(Enum):
    """花色"""
    HEARTS = "♥"      # 紅心
    DIAMONDS = "♦"    # 方塊
    CLUBS = "♣"       # 梅花
    SPADES = "♠"      # 黑桃


class Rank(Enum):
    """點數（名稱, 可能的點數值）"""
    ACE = ("A", [1, 11])      # A 可以是 1 或 11
    TWO = ("2", [2])
    THREE = ("3", [3])
    FOUR = ("4", [4])
    FIVE = ("5", [5])
    SIX = ("6", [6])
    SEVEN = ("7", [7])
    EIGHT = ("8", [8])
    NINE = ("9", [9])
    TEN = ("10", [10])
    JACK = ("J", [10])
    QUEEN = ("Q", [10])
    KING = ("K", [10])


@dataclass
class Card:
    """撲克牌"""
    suit: Suit
    rank: Rank
    
    def get_values(self) -> List[int]:
        """
        取得這張牌的可能點數
        大部分牌只有一個值，A 有兩個值 [1, 11]
        """
        return self.rank.value[1]
    
    def __str__(self) -> str:
        """字串表示，例如：A♠, K♥"""
        return f"{self.rank.value[0]}{self.suit.value}"
    
    def __repr__(self) -> str:
        return self.__str__()