import discord
import json
import os
from dump import initdump
from settings import WEBHOOK_FILE, TOKEN, CHANNEL_PATH, permissions, user_whitelist, compress_data
from datetime import date
import re
import hashlib
import random
import shutil
import requests


class MyBot(discord.Client):
    async def on_ready(self):
        print(f'Bot conectado como {self.user}')
        self.webhooks = {}
        if os.path.exists(WEBHOOK_FILE):
            with open(WEBHOOK_FILE, 'r', encoding='utf-8') as f:
                self.webhooks = json.load(f)
                print(f'Webhooks cargados: {self.webhooks}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not self.check_permissions(message) and message.content.startswith("!svb"):
            await message.channel.send("You don't have the permission to use this command.")
            return

        if message.content == "!svb setup":
            await self.setup_webhook(message.channel)
        elif message.content == "!svb save":
            await message.channel.send("Saving messages...")
            await self.save_messages(message.channel)
        elif message.content.startswith("!svb dump"):
            parts = message.content.split()
            if len(parts) != 3:
                await message.channel.send("Usage: !svb dump <channel_id>")
                return

            target_channel_id = int(parts[2])
            target_channel = self.get_channel(target_channel_id)
            if target_channel is None:
                await message.channel.send(f"No se pudo encontrar el canal con ID {target_channel_id}")
                return

            await self.setup_webhook(message.channel)
            await initdump(self.webhooks[str(message.channel.id)], target_channel_id)
        elif message.content == "!svb help":
            await message.channel.send("Comandos disponibles:\n!svb setup\n!svb save\n!svb dump <channel_id>")
        elif message.content.startswith("!svb"):
            await message.channel.send("Comando incorrecto. Usa !svb help para ver la lista de comandos disponibles.")
        else:
            await self.save_current_message(message.channel, message)

    def check_permissions(self, message):
        if permissions == "owner":
            return message.author.id == message.guild.owner_id
        elif permissions == "admins":
            return message.author.guild_permissions.administrator or message.author.id == message.guild.owner_id
        elif permissions == "whitelist":
            return message.author.id in user_whitelist
        elif permissions == "everyone":
            return True
        return False

    async def setup_webhook(self, channel):
        if str(channel.id) in self.webhooks:
            await channel.send(f'Ya existe un webhook para este canal')
            return

        webhook = await channel.create_webhook(name='SaveBot')
        self.webhooks[str(channel.id)] = webhook.url
        with open(WEBHOOK_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.webhooks, f, ensure_ascii=False, indent=4)
        await channel.send(f'Webhook creado')
        print(f'Webhook creado: {webhook.url}')

    async def save_current_message(self, channel, msg):
        channel_id = channel.id

        channel_time_path = f"{CHANNEL_PATH}/{channel_id}"
        if not os.path.exists(channel_time_path):
            os.makedirs(channel_time_path)

        json_file = f"{CHANNEL_PATH}/{channel_id}/{channel_id}_{date.today()}.json"

        try:
            with open(json_file) as f:
                json_file_content = json.load(f)
                message_data = json_file_content['data']
                avatars = json_file_content['avatars']
        except Exception as e:
            print(e)
            message_data = []
            avatars = {}

        user_id = msg.author.id
        if user_id not in avatars:
            avatars[user_id] = await self.get_avatar_url(msg.author)

        message_info = {
            'message_id': msg.id,
            'username': msg.author.name,
            'user_id': user_id,
            'content': msg.content,
            'timestamp': msg.created_at.isoformat(),
            'attachments': [attachment.url for attachment in msg.attachments],
            'referenced_message_id': msg.reference.message_id if msg.reference else None
        }

        message_data.append(message_info)

        regex = r"[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"

        for attachment in msg.attachments:
            url = attachment.url
            filename = re.search(regex, url)[0]

            response = requests.get(url, stream=True)
            with open(f"{CHANNEL_PATH}/{channel_id}/" + str(hashlib.md5(str(random.random()).encode()).hexdigest()) + str(filename) + '.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
    
        data_to_save = {
            'data': message_data,
            'avatars': avatars
        }
    
        with open(json_file, 'w', encoding='utf-8') as f:
            if compress_data:
                json.dump(data_to_save, f, ensure_ascii=False, separators=(',', ':'))
            else:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    
        

    async def save_messages(self, channel):
        
        channel_id = channel.id

        channel_time_path = f"{CHANNEL_PATH}/{channel_id}"
        if not os.path.exists(channel_time_path):
            os.makedirs(channel_time_path)

        json_file = f"{CHANNEL_PATH}/{channel_id}/{channel_id}_{date.today()}.json"

        print(f'Get messages in channel {channel.name}...')
        messages = []
        async for msg in channel.history(limit=None):
            messages.append(msg)
    
        messages.sort(key=lambda msg: msg.created_at)
    
        message_data = []
        avatars = {}
        for msg in messages:
            user_id = msg.author.id
            if user_id not in avatars:
                avatars[user_id] = await self.get_avatar_url(msg.author)
    
            message_info = {
                'message_id': msg.id,
                'username': msg.author.name,
                'user_id': user_id,
                'content': msg.content,
                'timestamp': msg.created_at.isoformat(),
                'attachments': [attachment.url for attachment in msg.attachments],
                'referenced_message_id': msg.reference.message_id if msg.reference else None
            }
            message_data.append(message_info)


            regex = r"[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"

            for attachment in msg.attachments:
                url = attachment.url
                filename = re.search(regex, url)[0]

                response = requests.get(url, stream=True)
                with open(f"{CHANNEL_PATH}/{channel_id}/" + str(hashlib.md5(str(random.random()).encode()).hexdigest()) + str(filename) + '.png', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response

    
        data_to_save = {
            'data': message_data,
            'avatars': avatars
        }
    
        with open(json_file, 'w', encoding='utf-8') as f:
            if compress_data:
                json.dump(data_to_save, f, ensure_ascii=False, separators=(',', ':'))
            else:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    
        print(f'Saved {len(messages)} messages')
        await channel.send(f'Saved {len(messages)} messages')

    async def get_avatar_url(self, user):
        return str(user.display_avatar.url)


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = MyBot(intents=intents)
client.run(TOKEN)