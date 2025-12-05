from app.game.game import Game

def play_game():
    """模擬一場遊戲"""
    game = Game()
    game.start_new_game()
    
    print("=== 21點遊戲開始 ===\n")
    
    # 顯示初始手牌
    print(f"玩家手牌: {game.player_hand}")
    print(f"莊家明牌: {game.dealer_hand.cards[0]}")
    print()
    
    # 檢查是否直接 Blackjack
    if game.player_hand.is_blackjack():
        print("🎉 玩家 Blackjack!")
        print(f"結果: {game.result.value}")
        return
    
    # 玩家決策（簡單 AI：< 17 就加牌）
    while game.status.value == "playing":
        player_value = game.player_hand.get_best_value()
        
        if player_value < 17:
            print(f"玩家點數 {player_value}，選擇加牌")
            can_continue = game.player_hit()
            print(f"玩家手牌: {game.player_hand}")
            
            if not can_continue:
                print("💥 玩家爆牌！")
                break
        else:
            print(f"玩家點數 {player_value}，選擇停牌")
            game.player_stand()
            break
        print()
    
    # 顯示最終結果
    if game.status.value == "finished":
        print("\n=== 遊戲結束 ===")
        print(f"玩家手牌: {game.player_hand}")
        print(f"莊家手牌: {game.dealer_hand}")
        print(f"\n結果: {game.result.value}")
        
        if game.result.value == "player_win":
            print("🎉 玩家獲勝！")
        elif game.result.value == "dealer_win":
            print("😢 莊家獲勝")
        else:
            print("🤝 平手")

# 玩 3 局
for i in range(3):
    print(f"\n{'='*50}")
    print(f"第 {i+1} 局")
    print('='*50)
    play_game()