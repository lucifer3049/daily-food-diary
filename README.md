> 每日飲食紀錄 Web App — 幫助你追蹤飲食習慣、管理健康目標。

## 專案簡介

這是我練習的一個追蹤每日飲食紀錄的 Web APP，幫助使用者紀錄今日所吃的食物和飲料，並且可以分析每日熱量，提出下一餐的飲食建議，希望能幫助使用者透過這個Web APP的功能，吃的健康。

## 功能特色

- 新增 / 編輯 / 刪除飲食紀錄
- 每日飲食熱量紀錄分析


## 技術架構

- 後端：Django + Python
- 前端 : Vue + Vite
- 資料庫:PostgreSQL
- 環境部屬: Vagrant + Docker
- AI工具: OpenAI
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

# 4. 進入虛擬機
vagrant ssh
cd /vagrant

# 5. 啟動 Docker 容器
docker-compose up --build

# 6. 執行資料庫 migration
docker-compose exec app python manage.py migrate

# 7. 建立管理員帳號（可選）
docker-compose exec app python manage.py createsuperuser

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


# 專案結構
daily-food-diary/
├── app/                  # Django 主應用程式
├── diary/                # 飲食紀錄模組
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Vagrantfile
└── .env