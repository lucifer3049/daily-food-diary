#!/bin/bash

echo "啟動虛擬機..."
vagrant up

echo "進入虛擬機..."
vagrant ssh -- -t "cd /vagrant && docker compose up -d && bash"

echo "完成! 已在http://localhost:8999"



