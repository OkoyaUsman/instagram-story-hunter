import os
import json
import time
import base64
import telebot
import curl_cffi
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

path = os.path.dirname(os.path.abspath(__file__))

ANONSTORIES_KEY = "LTE6Om11cmllbGdhbGxlOjpySlAydEJSS2Y2a3RiUnFQVUJ0UkU5a2xnQldiN2Q-"

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_USER_ID:
    raise ValueError('TELEGRAM_BOT_TOKEN and TELEGRAM_USER_ID must be set in the .env file')

def decode_url(url):
    b64_segment = urlparse(url).path.lstrip('/').split('/')[0]
    b64_segment += '=' * (-len(b64_segment) % 4)
    return base64.urlsafe_b64decode(b64_segment).decode('utf-8', errors='replace')

def load_data(file_name="data.json", empty=[]):
    f = os.path.join(path, file_name)
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    else:
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(empty, file)
        return empty

def save_data(data, file_name="data.json"):
    f = os.path.join(path, file_name)
    with open(f, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def log(*msg):
    log_entry = '[{:%d/%m/%Y - %H:%M:%S}] {}'.format(datetime.now(), msg[0])
    with open(os.path.join(path, "log.txt"), 'a', encoding="utf-8") as log_writer:
        log_writer.write(f"{log_entry}\n")
    print(log_entry)

def main():
    data = load_data()
    while True:
        log("Checking for new stories...")
        accounts_file = os.path.join(path, "accounts.txt")
        if not os.path.exists(accounts_file):
            with open(accounts_file, 'w', encoding='utf-8') as f:
                f.write("")
        with open(accounts_file, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip()]
        for username in usernames:
            log(f"Checking {username}")
            auth = base64.b64encode(f"-1::{username.lower().strip()}::{ANONSTORIES_KEY}".encode('utf-8'))
            content = curl_cffi.post("https://anonstories.com/api/v1/story", data={"auth": auth}, impersonate="chrome").json()
            for story in content["stories"]:
                try:
                    if story["media_type"] == "video":
                        video_url = decode_url(story["source"])
                        video_name = os.path.basename(urlparse(video_url).path)
                        if video_name and video_name not in data:
                            log(f"Found new status video from {username}")
                            tb = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
                            tb.send_video(chat_id=TELEGRAM_USER_ID, video=video_url, caption=f"New story from {username}")
                            data.append(video_name)
                            save_data(data)
                except Exception as e:
                    log(f"Error: {e}")
            time.sleep(2)
        log("Batch completed")
        time.sleep(600)

if __name__ == '__main__':
    main()