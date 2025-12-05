from enum import Enum
from typing import Optional
from .deck import Deck
from .hand import Hand


class GameStatus(Enum):
    """遊戲狀態"""
    IDLE = "idle"              # 閒置（等待開始）
    PLAYING = "playing"        # 進行中
    DEALER_TURN = "dealer_turn"  # 莊家回合
    FINISHED = "finished"      # 結束


class GameResult(Enum):
    """遊戲結果"""
    PLAYER_WIN = "player_win"
    DEALER_WIN = "dealer_win"
    PUSH = "push"              # 平手
    PLAYER_BLACKJACK = "player_blackjack"


class Game:
    """21點遊戲邏輯"""
    
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.status = GameStatus.IDLE
        self.result: Optional[GameResult] = None
    
    def start_new_game(self) -> None:
        """開始新遊戲"""
        # 重置狀態
        self.deck = Deck()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.status = GameStatus.PLAYING
        self.result = None
        
        # 發初始牌（玩家2張、莊家2張）
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        
        # 檢查玩家是否直接 Blackjack
        if self.player_hand.is_blackjack():
            self.status = GameStatus.FINISHED
            if self.dealer_hand.is_blackjack():
                self.result = GameResult.PUSH
            else:
                self.result = GameResult.PLAYER_BLACKJACK
    
    def player_hit(self) -> bool:
        """
        玩家加牌
        
        Returns:
            True: 可以繼續（沒爆牌）
            False: 爆牌了
        """
        if self.status != GameStatus.PLAYING:
            raise ValueError("遊戲狀態不正確，無法加牌")
        
        self.player_hand.add_card(self.deck.deal())
        
        if self.player_hand.is_bust():
            self.status = GameStatus.FINISHED
            self.result = GameResult.DEALER_WIN
            return False
        
        return True
    
    def player_stand(self) -> None:
        """玩家停牌，換莊家"""
        if self.status != GameStatus.PLAYING:
            raise ValueError("遊戲狀態不正確，無法停牌")
        
        self.status = GameStatus.DEALER_TURN
        self._dealer_play()
    
    def _dealer_play(self) -> None:
        """
        莊家自動補牌
        規則：< 17 必須補牌，>= 17 必須停牌
        """
        while self.dealer_hand.get_best_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())
        
        # 判定結果
        self._determine_winner()
        self.status = GameStatus.FINISHED
    
    def _determine_winner(self) -> None:
        """判定勝負"""
        player_value = self.player_hand.get_best_value()
        dealer_value = self.dealer_hand.get_best_value()
        
        # 莊家爆牌
        if self.dealer_hand.is_bust():
            self.result = GameResult.PLAYER_WIN
        # 玩家點數較大
        elif player_value > dealer_value:
            self.result = GameResult.PLAYER_WIN
        # 莊家點數較大
        elif dealer_value > player_value:
            self.result = GameResult.DEALER_WIN
        # 平手
        else:
            self.result = GameResult.PUSH
    
    def get_game_state(self) -> dict:
        """取得當前遊戲狀態（用於 API 回傳）"""
        return {
            "status": self.status.value,
            "result": self.result.value if self.result else None,
            "player_hand": {
                "cards": [str(card) for card in self.player_hand.cards],
                "value": self.player_hand.get_best_value(),
                "is_bust": self.player_hand.is_bust(),
                "is_blackjack": self.player_hand.is_blackjack()
            },
            "dealer_hand": {
                "cards": [str(card) for card in self.dealer_hand.cards],
                "value": self.dealer_hand.get_best_value() if self.status == GameStatus.FINISHED else "?",
                "is_bust": self.dealer_hand.is_bust() if self.status == GameStatus.FINISHED else False
            }
        }