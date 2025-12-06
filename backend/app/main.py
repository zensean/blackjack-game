import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.api.connection_manager import manager
from fastapi.responses import HTMLResponse

# --- 這裡 import 你剛剛提供的 OOD 核心邏輯 ---
# 確保 app/game 資料夾裡有 __init__.py，這樣 Python 才找得到
from app.game.game import Game

app = FastAPI(
    title="Blackjack Game API",
    description="21點線上遊戲後端 API (WebSocket MVP)",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- [關鍵] 全域遊戲實例 (Global State) ---
# 為了 MVP 展示，我們讓所有連線進來的人都在玩「同一局」
# 這能展現最強的 WebSocket 特性：A 玩家按「要牌」，B 玩家的畫面也會同步更新！
global_game = Game()

@app.get("/", response_class=HTMLResponse)
async def root():
    # 這裡假設 index.html 跟 main.py (或 Docker 的工作目錄) 在同一層
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    # 1. 建立連線
    await manager.connect(websocket)
    
    try:
        # 剛連線時，廣播歡迎訊息
        await manager.broadcast(f"🔴 系統廣播: 玩家 {client_id} 加入了戰局！")
        
        while True:
            # 2. 接收指令 (start, hit, stand)
            data = await websocket.receive_text()
            cmd = data.strip().lower() # 轉小寫，容錯
            
            response_msg = ""
            
            # --- 3. 呼叫你的 Game 邏輯 ---
            
            if cmd == "start":
                global_game.start_new_game()
                # 取得第一張明牌 (Dealer 的第一張)
                dealer_first_card = global_game.dealer_hand.cards[0]
                
                # ★★★ [Bug 修復重點] 檢查是否起手 Blackjack ★★★
                if global_game.status.value == "finished":
                    # 遊戲瞬間結束 (有人拿到 Blackjack)
                    result_map = {
                        "player_win": "🎉 玩家獲勝！",
                        "dealer_win": "😢 莊家獲勝",
                        "push": "🤝 平手 (Push)",
                        "player_blackjack": "✨ 運氣爆棚！天胡 BlackJack！"
                    }
                    result_text = result_map.get(global_game.result.value, global_game.result.value)
                    
                    response_msg = (
                        f"📢 隊友 {client_id} 開啟新局... 什麼！？\n"
                        f"⚡ 竟然起手就結束了！\n"
                        f"----------------\n"
                        f"😈 莊家手牌: {global_game.dealer_hand}\n"
                        f"🛡️ 團隊手牌: {global_game.player_hand}\n"
                        f"----------------\n"
                        f"🏆 最終結果: {result_text}"
                    )
                else:
                    # 遊戲正常進行中
                    response_msg = (
                        f"📢 隊友 {client_id} 宣佈遊戲開始！\n"
                        f"😈 莊家明牌: [{dealer_first_card}] (?)\n"
                        f"🛡️ 團隊手牌: {global_game.player_hand}"
                    )

            elif cmd == "hit":
                if global_game.status.value != "playing":
                    await manager.send_personal_message("⚠️ 遊戲尚未開始或已結束，請輸入 start", websocket)
                    continue
                
                # 執行要牌
                is_safe = global_game.player_hit()
                
                if is_safe:
                    response_msg = (
                        f"⚔️ 隊友 {client_id} 決定加牌！\n"
                        f"✅ 成功！目前團隊點數: {global_game.player_hand.get_best_value()}\n"
                        f"牌面: {global_game.player_hand}"
                    )
                else:
                    # 爆牌了
                    response_msg = (
                        f"💀 隊友 {client_id} 按下了要牌...\n"
                        f"💥 團隊爆牌了！ ({global_game.player_hand})\n"
                        f"💸 本局結束，莊家獲勝。\n"
                        f"🏆 最終結果: 莊家獲勝" 
                    )

            elif cmd == "stand":
                if global_game.status.value != "playing":
                    await manager.send_personal_message("⚠️ 無法停牌", websocket)
                    continue
                
                # 執行停牌 (會自動跑莊家邏輯)
                global_game.player_stand()
                
                # 遊戲結束，顯示結果
                result_map = {
                    "player_win": "🎉 玩家獲勝！",
                    "dealer_win": "😢 莊家獲勝",
                    "push": "🤝 平手 (Push)",
                    "player_blackjack": "✨ BlackJack! 玩家獲勝！"
                }
                result_text = result_map.get(global_game.result.value, global_game.result.value)
                
                response_msg = (
                    f"🛑 隊友 {client_id} 認為點數夠了，選擇停牌！\n"
                    f"----------------\n"
                    f"😈 莊家開牌: {global_game.dealer_hand}\n"
                    f"🛡️ 團隊手牌: {global_game.player_hand}\n"
                    f"----------------\n"
                    f"🏆 最終結果: {result_text}"
                )

            else:
                response_msg = f"❓ 未知指令: {cmd} (請輸入 start, hit, 或 stand)"

            # 4. 廣播給所有人 (State Sync)
            await manager.broadcast(response_msg)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"⚪ 系統廣播: 玩家 {client_id} 離開了遊戲")
    except Exception as e:
        # 捕捉邏輯錯誤
        print(f"Error: {e}")
        await manager.broadcast(f"⚠️ 系統錯誤: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)