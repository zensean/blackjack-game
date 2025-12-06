# 1. 基底：使用官方 Python 3.9 輕量版
FROM python:3.9-slim

# 2. 設定工作目錄
WORKDIR /app

# 3. 複製需求清單
COPY requirements.txt .

# 4. 安裝套件 (不使用快取以減小體積)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製剩下的程式碼
COPY . .

# 6. 宣告 Port
EXPOSE 8000

# 7. 啟動指令 (Host 設為 0.0.0.0 才能讓外部存取)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]