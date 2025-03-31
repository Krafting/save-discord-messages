
# SaveBot - Discord Message Backup Bot

SaveBot is a Discord bot designed to backup messages from Discord channels. It allows you to save every messages and images from a channel to a JSON file.

## Table of Contents
- [Documentation](#documentation)
  - [Settings](#settings)
  - [Commands](#commands)
  - [Usage Examples](#usage-examples)

- [Linux Installation](#linux-installation)

## Documentation

### Settings

The bot's settings are configured in the `settings.json` file. Here's an explanation of each setting:

- `use_env_variable` (boolean): If set to `true`, the bot will use the `DISCORD_BOT_TOKEN` environment variable for the token. If `false`, it will use the token specified in the `token` field.
- `token` (string): Your Discord bot token. Only used if `use_env_variable` is `false`.
- `saved_channels_path` (string): The directory path where channel backups will be saved.
- `webhooks_file` (string): The file path where webhook information will be stored.
- `only_owner` (boolean): If `true`, only the server owner can use the bot commands.
- `only_admins` (boolean): If `true`, only server administrators can use the bot commands.
- `enable_user_whitelist` (boolean): If `true`, only users in the `user_whitelist` can use the bot commands.
- `user_whitelist` (array): An array of user IDs allowed to use the bot when `enable_user_whitelist` is `true`.
- `hour_region` (string): The timezone used for displaying message timestamps (e.g., "Europe/Madrid").

### Commands

SaveBot supports the following commands:

1. `!svb setup`: Creates a webhook for the current channel.
2. `!svb save`: Saves all messages from the current channel to a JSON file.
4. `!svb help`: Displays a list of available commands.

### Usage Examples

1. Setting up a webhook for the current channel (does nothing):
   ```
   !svb setup
   ```

2. Saves all previous messages from the current channel:
   ```
   !svb save
   ```

4. Displaying help information:
   ```
   !svb help
   ```

5. Every messages sent to a channel where the bot is invited will be saved automatically

## Linux Installation

This method has been tested on a `Debian 12 LXC container`.

To install Python 3.11 and create a virtual environment with dependencies from `requirements.txt`, execute the following command in your terminal:

```bash
cd /opt
git clone https://github.com/Krafting/save-discord-messages
cd save-discord-messages
sudo apt update && sudo apt install -y python3.11 python3.11-venv 
python3.11 -m venv .venv
source .venv/bin/activate && pip install -r requirements.txt

# Auto start service
sudo cp discord-bot.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now discord-bot.service
```

This command does the following:
0. Clone this repo and enter the folder
1. Updates the package list.
2. Installs Python 3.11 and the virtual environment module.
3. Creates a virtual environment named `.venv`.
4. Activates the virtual environment.
5. Installs the dependencies specified in `requirements.txt`.
6 (Optionnal). Enable a service that start the bot at boot

**Don't forget to copy the `settings.example.json` to `settings.json` and edit the `token` option with your discord bot token**

