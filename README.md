# 🎮 Blackjack Game - 21點線上遊戲

## 專案簡介
使用 Python FastAPI + Vue 3 打造的全端 21點卡牌遊戲

## 技術棧
- **後端**: FastAPI, PostgreSQL, Redis
- **前端**: Vue 3, Vite, Pinia
- **部署**: AWS EC2, Docker, Nginx

## 開發進度
- [x] Phase 1.1: 專案環境建置
- [ ] Phase 1.2: 遊戲邏輯設計
- [ ] Phase 1.3: 遊戲邏輯實作
- [ ] Phase 2: 資料庫 + API
- [ ] Phase 3: 前端開發
- [ ] Phase 4: 部署
- [ ] Phase 5: CI/CD

## 本地開發

### 後端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

訪問 http://127.0.0.1:8000/docs 查看 API 文件

## 作者
Sean - Junior Backend Engineer