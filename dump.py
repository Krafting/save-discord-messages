import requests
import json
import time
import datetime
from utc import convertir_timestamp



def send_webhook_message(webhook_url, username, avatar_url, content, attachments, date):
    data = {
        'username': username,
        'avatar_url': avatar_url,
        'content': convertir_timestamp(date) + "\n " + content,
    }
    

    if attachments:
        data['content'] += '\n' + '\n'.join(attachments)

    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f'Error al enviar el mensaje: {err}')
        print(data)
        if err.response.status_code == 429:
            print('Rate limited. Esperando 1 segundo...')
            time.sleep(5)
            send_webhook_message(webhook_url, username, avatar_url, content, attachments, date)
    else:
        print(f'Mensaje enviado correctamente: {result.status_code}')





async def initdump(webhook_url, channel_id):
    with open(f"saves/{channel_id}.json", 'r', encoding='utf-8') as f:
        messages = json.load(f)
    data = messages['data']
    avatars = messages['avatars']
    for msg in data:
        avatar_url = avatars.get(str(msg['user_id']), '')
        send_webhook_message(webhook_url, msg['username'], avatar_url, msg['content'], msg['attachments'], msg['timestamp'])