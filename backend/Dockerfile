# 1. 基底：使用官方 Python 3.9 輕量版
FROM python:3.9-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 複製需求清單
# 注意：因為我們會在最外層執行 build，所以路徑要加上 backend/
COPY backend/requirements.txt .

# 4. 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製後端程式碼
# 將 backend 資料夾內的所有東西 (包含 app/, main.py 等) 複製到容器的 /app
COPY backend/ .

# 6. 關鍵步驟：複製前端檔案
# 將 frontend 資料夾複製到容器內的 /app/frontend
# 這樣 Python 往上一層找的時候就找得到了！
COPY frontend/ /app/frontend/

# 7. 宣告 Port
EXPOSE 8000

# 8. 啟動指令 (Host 設為 0.0.0.0 才能讓外部存取)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]