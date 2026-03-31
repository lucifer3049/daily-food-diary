# instruction.sh 指令碼筆記
vagrant up # 啟動虛擬機
vagrant ssh # 進入虛擬機
vagrant halt # 關閉虛擬機

vagrant reload # 重啟虛擬機

ls /vagrant #列出專案目錄

cd /vagrant # 進入專案目錄

docker compose run web django-admin startproject my_daily_food # 建立專案

docker compose up -d # 啟動專案
docker compose up --build  # 啟動專案 重新建置

exit # 退出虛擬機

# 管理者權限更新套件在VM裡面執行
sudo apt-get update
sudo apt-get install -y linux-headers-$(uname -r) build-essential dkms virtualbox-guest-utils

sudo apt-get install -y virtualbox-guest-utils
sudo mount -t vbox sf_vagrant /vagrant # 掛載資料夾到VM

# 安裝pip
sudo apt update
sudo apt install -y python3-pip
pip3 --version # 確認安裝成功

docker compose up -d # 啟動docker
docker compose down # 停止docker
docker compose logs -f # 查看docker log
docker compose exec web bash # 進入django
docker exec -it vagrant-web-1 python manage.py migrate  # 在Django container 裡面建立資料庫

# Django 
python3 -c "from django.core.signing import get_cookie_signer; from django.utils.crypto import get_random_string; print(get_random_string(50))"  # django 產生密鑰

python3 manage.py createsuperuser # 建立管理者帳號