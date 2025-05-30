import discord
import json
import os
from settings import WEBHOOK_FILE, TOKEN, CHANNEL_PATH, permissions, user_whitelist, compress_data
from datetime import date
import re
import hashlib
import random
import shutil
import requests


class MyBot(discord.Client):
    async def on_ready(self):
        print(f'Bot connected to {self.user}')
        self.webhooks = {}
        if os.path.exists(WEBHOOK_FILE):
            with open(WEBHOOK_FILE, 'r', encoding='utf-8') as f:
                self.webhooks = json.load(f)
                print(f'Webhooks loaded: {self.webhooks}')

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
        elif message.content == "!svb help":
            await message.channel.send("Available commands:\n!svb setup\n!svb save")
        elif message.content.startswith("!svb"):
            await message.channel.send("Incorrect command. Use !svb to see the list of available commands.")
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
            await channel.send(f'A webhook already exists for this channel.')
            return

        webhook = await channel.create_webhook(name='SaveBot')
        self.webhooks[str(channel.id)] = webhook.url
        with open(WEBHOOK_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.webhooks, f, ensure_ascii=False, indent=4)
        await channel.send(f'Webhook created')
        print(f'Webhook created: {webhook.url}')

    async def save_current_message(self, channel, msg):
        channel_id = channel.id

        channel_time_path = f"{CHANNEL_PATH}/{channel.name}-{channel_id}"
        if not os.path.exists(channel_time_path):
            os.makedirs(channel_time_path)

        json_file = f"{CHANNEL_PATH}/{channel.name}-{channel_id}/{channel_id}_{date.today()}.json"

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
            'attachments_refs': [],
            'referenced_message_id': msg.reference.message_id if msg.reference else None
        }


        regex = r"[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"

        for attachment in msg.attachments:
            url = attachment.url
            filename = re.search(regex, url)[0]

            random_hash = str(hashlib.md5(str(random.random()).encode()).hexdigest())
            message_info['attachments_refs'].append(random_hash)

            response = requests.get(url, stream=True)
            with open(f"{CHANNEL_PATH}/{channel.name}-{channel_id}/" + random_hash + '-' + str(filename), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

        message_data.append(message_info)
    
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

        channel_time_path = f"{CHANNEL_PATH}/{channel.name}-{channel_id}"
        if not os.path.exists(channel_time_path):
            os.makedirs(channel_time_path)

        json_file = f"{CHANNEL_PATH}/{channel.name}-{channel_id}/{channel_id}_{date.today()}.json"

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
                'attachments_refs': [],
                'referenced_message_id': msg.reference.message_id if msg.reference else None
            }


            regex = r"[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"

            for attachment in msg.attachments:
                url = attachment.url
                filename = re.search(regex, url)[0]

                random_hash = str(hashlib.md5(str(random.random()).encode()).hexdigest())
                message_info['attachments_refs'].append(random_hash)
                
                response = requests.get(url, stream=True)
                with open(f"{CHANNEL_PATH}/{channel.name}-{channel_id}/" + random_hash +  '-' + str(filename), 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response

            message_data.append(message_info)
    
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
        """
        Get user Avatar
        """
        return str(user.display_avatar.url)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = MyBot(intents=intents)
client.run(TOKEN)