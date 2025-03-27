#!/usr/bin/bash
cd /opt/save-discord-messages

python3.11 -m venv .venv
source .venv/bin/activate

python3.11 main.py