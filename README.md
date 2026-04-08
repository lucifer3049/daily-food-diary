> 每日飲食紀錄 Web App — 幫助你追蹤飲食習慣、管理健康目標。

## 專案簡介

這是我練習的一個追蹤每日飲食紀錄的 Web APP，幫助使用者紀錄今日所吃的食物和飲料，並且可以分析每日熱量，提出下一餐的飲食建議，希望能幫助使用者透過這個Web APP的功能。

## 功能特色

- 新增 / 編輯 / 刪除飲食紀錄
- 每日飲食熱量紀錄分析


## 技術架構
- 作業系統: vagrant(Ubuntu Jammy) 
- 容器化: Docker & Docker Compose
- 後端: Django + Python
- 前端: Vue + Vite
- 資料庫: PostgreSQL
- AI工具: OpenAI + claude + gemini 
- 版本控制: Git + GitHub


### 環境需求
- Python 3.12

### 安裝步驟

# 1. Clone 專案
git clone https://github.com/lucifer3049/daily-food-diary.git
cd daily-food-diary

# 2. 複製環境變數範本並填入設定
cp .env.example .env

# 3. 啟動 Vagrant 虛擬機
vagrant up

# 4. 進入 Vagrant 虛擬機
vagrant ssh
cd /vagrant

# 5. 啟動 Docker 容器
docker compose up -d

# 6. 建立遷移擋
# 開發新功能必做，初次安裝可以跳過此步驟
docker compose exec web python3 manage.py makemigrations

# 7. 執行資料庫 migration 將新功能加入資料庫
docker compose exec web python3 manage.py migrate

# 8. 建立管理員帳號（可選）
docker-compose exec web python manage.py createsuperuser

# 9. 查看日誌
docker compose logs -f web

# 10. 讓 Docker 重新讀取 requirements.txt
docker compose up -d --build

# 11. Docker 檢查 import 或語法錯誤
docker compose exec web python3 manage.py check

# 12. 執行測試腳本
docker compose exec web python3 manage.py test

打開瀏覽器前往 `http://localhost:8999` 即可使用。

## 環境變數說明
# Django
SECRET_KEY # Django 密鑰
DEBUG # Debug 模式（開發時設為 True）
ALLOWED_HOSTS # 允許的主機 例如 localhost,127.0.0.1

# PostgreSQL
DB_NAME # DB名稱
DB_USER # DB使用者
DB_PASSWORD # DB密碼
DB_HOST # DB主機 （Docker 內通常為 db）
DB_PORT # DB連接埠 （預設 5432）

# AI API
OPEN_AI_KEY # API金鑰 


## 專案目錄結構

```text
.
├── Vagrantfile               # 虛擬機配置文件
├── docker-compose.yml        # Docker 服務定義
├── Dockerfile                # Python 環境構建檔
├── requirements.txt          # Python 套件清單 (含 Pillow, Django 等)
├── app/                      # Django 專案核心設定 (Project Root)
│   ├── settings.py           # 全域設定 (時區、語系、App 註冊)
│   └── urls.py               # 全域路由入口
└── diary/                    # 飲食紀錄主要應用程式 (Django App)
    ├── admin.py              # 後台管理配置
    ├── models/               # 資料模型層 (拆分封裝)
    │   ├── __init__.py       # 統一匯出 Model 類別
    │   └── food_diary_models.py
    ├── forms/                # 表單處理層
    │   ├── __init__.py       # 匯出 Form 類別
    │   └── food_entry_form.py
    ├── views/                # 業務邏輯層
    │   ├── __init__.py
    │   └── views.py          # 處理請求與回傳回應
    ├── templates/            # 前端模板 (HTML)
    ├── migrations/           # 資料庫遷移紀錄
    └── tests/                # 單元測試