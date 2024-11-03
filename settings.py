import json
import os

with open('settings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if data.get("use_env_variable"):
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
else:
    TOKEN = data["token"]
    CHANNEL_PATH = data["saved_channels_path"]
    WEBHOOK_FILE = data["webhooks_file"]
    HOUR_REGION = data["hour_region"]
    
    only_owner = data["only_owner"]
    only_admins = data["only_admins"]
    enable_user_whitelist = data["enable_user_whitelist"]
    user_whitelist = data["user_whitelist"]
    
    if only_owner:
        only_admins = False
        enable_user_whitelist = False
        permissions = "owner"
    elif only_admins:
        enable_user_whitelist = False
        permissions = "admins"
    elif enable_user_whitelist:
        permissions = "whitelist"
    elif not only_owner and not only_admins and not enable_user_whitelist:
        permissions = "everyone"
    user_whitelist = data["user_whitelist"]