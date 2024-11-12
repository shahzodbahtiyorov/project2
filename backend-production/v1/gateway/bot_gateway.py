import requests

from config_env import base


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{base.BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': base.GROUP_ID,
        'text': message,
        # 'message_thread_id': 11,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    return response
