# Vagrantfile
Vagrant.configure("2") do |config| # 建立虛擬機
  config.vm.box = "ubuntu/jammy64"  # 作業系統

  # 網路設定
  config.vm.network "private_network", ip: "192.168.56.108" # VM的虛擬IP
  config.vm.network "forwarded_port", guest: 8999, host: 8999  # Django
  config.vm.network "forwarded_port", guest: 5444, host: 5444  # PostgreSQL

  config.vm.synced_folder ".", "/vagrant"  # 本機資料夾同步到虛擬機


  config.vm.provider "virtualbox" do |vb| # 設定虛擬機CPU與記憶體
    vb.memory = "2048"
    vb.cpus = 2
  end

  # 自動安裝 Docker
  config.vm.provision "shell", inline: <<-SHELL
    # 安裝 Docker
    apt-get update
    apt-get install -y ca-certificates curl gnupg

    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    # 讓 vagrant 使用者可以執行 docker（不需要 sudo）
    usermod -aG docker vagrant

    echo "Docker 安裝完成！"
  SHELL
end