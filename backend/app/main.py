from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Blackjack Game API",
    description="21點線上遊戲後端 API",
    version="0.1.0"
)

# CORS 設定（讓前端可以呼叫 API）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發時允許所有來源，生產環境要改
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Blackjack Game API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}