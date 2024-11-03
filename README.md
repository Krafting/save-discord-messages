
# SaveBot - Discord Message Backup Bot

SaveBot is a Discord bot designed to backup and restore messages from Discord channels. It allows you to save messages from a channel to a JSON file and later restore them to another channel using webhooks.

## Table of Contents
- [English Documentation](#english-documentation)
  - [Settings](#settings)
  - [Commands](#commands)
  - [Usage Examples](#usage-examples)
- [Documentación en Español](#documentación-en-español)
  - [Configuración](#configuración)
  - [Comandos](#comandos)
  - [Ejemplos de Uso](#ejemplos-de-uso)
- [Linux Installation](#linux-installation)
- [Windows Installation](#windows-installation)
- [Mac Installation](#mac-installation)

## English Documentation

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
3. `!svb dump <channel_id>`: Restores messages from a saved JSON file to the specified channel.
4. `!svb help`: Displays a list of available commands.

### Usage Examples

1. Setting up a webhook for the current channel:
   ```
   !svb setup
   ```

2. Saving messages from the current channel:
   ```
   !svb save
   ```

3. Restoring messages to a different channel:
   ```
   !svb dump 123456789012345678
   ```
   Replace `123456789012345678` with the target channel ID.

4. Displaying help information:
   ```
   !svb help
   ```

## Documentación en Español

### Configuración

La configuración del bot se realiza en el archivo `settings.json`. Aquí se explica cada configuración:

- `use_env_variable` (booleano): Si es `true`, el bot usará la variable de entorno `DISCORD_BOT_TOKEN` para el token. Si es `false`, usará el token especificado en el campo `token`.
- `token` (cadena): Tu token de bot de Discord. Solo se usa si `use_env_variable` es `false`.
- `saved_channels_path` (cadena): La ruta del directorio donde se guardarán las copias de seguridad de los canales.
- `webhooks_file` (cadena): La ruta del archivo donde se almacenará la información de los webhooks.
- `only_owner` (booleano): Si es `true`, solo el propietario del servidor puede usar los comandos del bot.
- `only_admins` (booleano): Si es `true`, solo los administradores del servidor pueden usar los comandos del bot.
- `enable_user_whitelist` (booleano): Si es `true`, solo los usuarios en la `user_whitelist` pueden usar los comandos del bot.
- `user_whitelist` (array): Un array de IDs de usuario permitidos para usar el bot cuando `enable_user_whitelist` es `true`.
- `hour_region` (cadena): La zona horaria utilizada para mostrar las marcas de tiempo de los mensajes (por ejemplo, "Europe/Madrid").

### Comandos

SaveBot admite los siguientes comandos:

1. `!svb setup`: Crea un webhook para el canal actual.
2. `!svb save`: Guarda todos los mensajes del canal actual en un archivo JSON.
3. `!svb dump <channel_id>`: Restaura los mensajes de un archivo JSON guardado al canal especificado.
4. `!svb help`: Muestra una lista de comandos disponibles.

### Ejemplos de Uso

1. Configurar un webhook para el canal actual:
   ```
   !svb setup
   ```

2. Guardar mensajes del canal actual:
   ```
   !svb save
   ```

3. Restaurar mensajes a un canal diferente:
   ```
   !svb dump 123456789012345678
   ```
   Reemplaza `123456789012345678` con el ID del canal de destino.

4. Mostrar información de ayuda:
   ```
   !svb help
   ```


## Linux Installation

To install Python 3.10.15 and create a virtual environment with dependencies from `requirements.txt`, execute the following command in your terminal:

```bash
sudo apt update && sudo apt install -y python3.10 python3.10-venv && python3.10 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

This command does the following:
1. Updates the package list.
2. Installs Python 3.10 and the virtual environment module.
3. Creates a virtual environment named `.venv`.
4. Activates the virtual environment.
5. Installs the dependencies specified in `requirements.txt`.

## Windows Installation

### Step 1: Download and Install Python 3.10.15
1. Go to the [official Python downloads page](https://www.python.org/downloads/release/python-31015/).
2. Download the Windows installer for Python 3.10.15.
3. Run the installer and make sure to check the box that says "Add Python to PATH".
4. Follow the installation prompts to complete the installation.

### Step 2: Create a Virtual Environment
1. Open Command Prompt (cmd).
2. Navigate to your project directory using the `cd` command.
3. Run the following commands:

```cmd
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
Run the following command to activate the virtual environment:

```cmd
.\.venv\Scripts\activate
```

### Step 4: Install Dependencies
With the virtual environment activated, run:

```cmd
pip install -r requirements.txt
```

## Mac Installation

### Step 1: Download and Install Python 3.10.15
1. Go to the [official Python downloads page](https://www.python.org/downloads/release/python-31015/).
2. Download the macOS installer for Python 3.10.15.
3. Run the installer and follow the installation prompts.

### Step 2: Create a Virtual Environment
1. Open Terminal.
2. Navigate to your project directory using the `cd` command.
3. Run the following commands:

```bash
python3.10 -m venv .venv
```

### Step 3: Activate the Virtual Environment
Run the following command to activate the virtual environment:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies
With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```
