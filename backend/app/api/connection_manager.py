from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # 這裡用來存「目前所有連線中的人」
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """當有新玩家連線時，把他加入名單"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """當玩家斷線時，把他移出名單"""
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """只傳訊息給特定一個人 (例如：你贏了)"""
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """廣播給所有人 (例如：莊家發牌了，大家的畫面都要更新)"""
        for connection in self.active_connections:
            await connection.send_text(message)

# 實體化這個 Manager，讓其他地方可以 import 使用
manager = ConnectionManager()