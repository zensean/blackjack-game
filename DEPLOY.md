# 🚀 Blackjack 21點專案 - 部署指南

本文件記錄了如何在 AWS EC2 上手動更新與部署 Blackjack 專案的完整流程。

---

## 📋 前置資訊

### 環境配置
- **本地端環境:** VS Code, Git
- **雲端環境:** AWS EC2 (Ubuntu), Docker, Nginx
- **Docker 映像檔名稱:** `blackjack-app`
- **Docker 容器名稱:** `blackjack-backend-main`
- **服務端口 (Port):** `8000`

### 架構說明
本專案採用前後端分離架構，使用 Docker 容器化部署：
- Frontend 位於 `frontend/` 目錄
- Backend 位於 `backend/` 目錄
- Dockerfile 位於 `backend/Dockerfile`
- 建置時需在專案根目錄執行，以包含 frontend 資源

---

## 🔄 完整部署流程

### 步驟 1：本地端 Git 操作

#### 1.1 暫存所有修改
```bash
# 將所有修改過的檔案加入追蹤（包含 index.html, Dockerfile, main.py 等）
git add .
```

#### 1.2 提交變更
```bash
# 提交修改並撰寫有意義的 commit message
git commit -m "feat: 更新功能說明"
```

#### 1.3 推送到 GitHub
```bash
# 推送到 GitHub 遠端儲存庫
git push
```

---

### 步驟 2：連接 EC2 並拉取更新

#### 2.1 切換到專案根目錄
```bash
# 回到專案根目錄（確保能看到 backend 和 frontend 兩個資料夾）
cd ~/blackjack-game
```

#### 2.2 拉取最新代碼
```bash
# 從 GitHub 拉取最新的代碼
git pull
```

---

### 步驟 3：重新建置 Docker 映像檔

#### 3.1 建置新映像檔
```bash
# 在專案根目錄建立 Docker 映像檔
# -f backend/Dockerfile: 指定 Dockerfile 位置
# -t blackjack-app: 指定映像檔名稱（tag）
# . : 指定建置上下文為當前目錄（包含 frontend）
sudo docker build -f backend/Dockerfile -t blackjack-app .
```

**參數說明：**
| 參數 | 說明 |
|------|------|
| `-f backend/Dockerfile` | 指定 Dockerfile 的路徑 |
| `-t blackjack-app` | 為映像檔命名（tag） |
| `.` | 建置上下文路徑（當前目錄） |

---

### 步驟 4：部署新容器

#### 4.1 停止並刪除舊容器
```bash
# 強制刪除舊的容器實例
sudo docker rm -f blackjack-backend-main
```

#### 4.2 啟動新容器
```bash
# 啟動新的容器實例
# -d: 背景運行（detached mode）
# -p 127.0.0.1:8000:8000: 端口映射（僅本地訪問）
# --name blackjack-backend-main: 容器名稱
# blackjack-app: 使用的映像檔
sudo docker run -d -p 127.0.0.1:8000:8000 --name blackjack-backend-main blackjack-app
```

**參數說明：**
| 參數 | 說明 |
|------|------|
| `-d` | 背景模式運行 |
| `-p 127.0.0.1:8000:8000` | 將容器 8000 端口映射到主機 127.0.0.1:8000（安全設定） |
| `--name blackjack-backend-main` | 指定容器名稱 |
| `blackjack-app` | 使用的 Docker 映像檔 |

---

### 步驟 5：驗證部署狀態

```bash
# 查看所有正在運行的容器
sudo docker ps

# 查看特定容器的日誌（檢查是否有錯誤）
sudo docker logs blackjack-backend-main

# 查看容器的最新 20 行日誌
sudo docker logs --tail 20 blackjack-backend-main
```

---

## ⏮️ 回滾步驟

如果新版本出現問題，可以透過以下方式回滾到前一個版本：

### 方法 1：使用 Git 回滾

#### 1.1 查看 commit 歷史
```bash
# 查看最近的 commit 記錄
git log --oneline -5
```

#### 1.2 回退到指定版本
```bash
# 回退到上一個 commit
git reset --hard HEAD~1

# 或回退到特定 commit hash
git reset --hard <commit-hash>
```

#### 1.3 重新部署
```bash
# 執行步驟 3 和步驟 4 重新建置並部署
sudo docker build -f backend/Dockerfile -t blackjack-app .
sudo docker rm -f blackjack-backend-main
sudo docker run -d -p 127.0.0.1:8000:8000 --name blackjack-backend-main blackjack-app
```

### 方法 2：使用舊的 Docker 映像檔

#### 2.1 查看所有映像檔
```bash
# 列出所有 Docker 映像檔（包含舊版本）
sudo docker images
```

#### 2.2 使用舊映像檔啟動容器
```bash
# 停止並刪除當前容器
sudo docker rm -f blackjack-backend-main

# 使用舊的映像檔 ID 啟動容器
sudo docker run -d -p 127.0.0.1:8000:8000 --name blackjack-backend-main <舊映像檔ID>
```

---

## 📚 常用指令速查表

### Docker 容器管理
```bash
# 查看運行中的容器
sudo docker ps

# 查看所有容器（包含停止的）
sudo docker ps -a

# 停止容器
sudo docker stop blackjack-backend-main

# 啟動已停止的容器
sudo docker start blackjack-backend-main

# 重啟容器
sudo docker restart blackjack-backend-main

# 刪除容器
sudo docker rm blackjack-backend-main

# 強制刪除運行中的容器
sudo docker rm -f blackjack-backend-main
```

### Docker 映像檔管理
```bash
# 查看所有映像檔
sudo docker images

# 刪除映像檔
sudo docker rmi blackjack-app

# 刪除所有未使用的映像檔
sudo docker image prune -a
```

### 日誌查看
```bash
# 查看容器日誌
sudo docker logs blackjack-backend-main

# 即時查看日誌（follow mode）
sudo docker logs -f blackjack-backend-main

# 查看最新 N 行日誌
sudo docker logs --tail 50 blackjack-backend-main
```

### 進入容器內部
```bash
# 進入容器的 bash shell
sudo docker exec -it blackjack-backend-main bash

# 執行單一命令
sudo docker exec blackjack-backend-main ls -la
```

---

## 💡 注意事項

1. **安全性設定：** 端口綁定使用 `127.0.0.1:8000:8000` 確保服務僅能從本機訪問，對外訪問需透過 Nginx 反向代理
2. **建置位置：** 必須在專案根目錄 (`~/blackjack-game`) 執行 Docker build，而非在 `backend/` 目錄內
3. **容器命名：** 統一使用 `blackjack-backend-main` 作為容器名稱，避免混淆
4. **日誌監控：** 部署後記得查看日誌確認服務正常啟動
5. **映像檔清理：** 定期清理未使用的舊映像檔以節省磁碟空間

---

最後更新日期：2025-12-07