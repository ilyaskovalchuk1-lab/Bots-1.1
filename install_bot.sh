#!/bin/bash
sudo apt update && sudo apt install -y python3-pip
pip install -r requirements.txt
nohup python3 bot.py > bot.log 2>&1 &
