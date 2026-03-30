#!/bin/bash

echo "關閉docker..."
vagrant ssh -- -t "cd /vagrant && docker compose down"

echo "停止虛擬機..."
vagrant halt

echo "關閉了"