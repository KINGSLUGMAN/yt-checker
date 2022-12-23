import time, threading, requests
from fake_useragent import UserAgent
import random
import socket
import struct
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

usernames = []
users = open('usernames.txt', 'r')

with open('avail.txt', 'r') as file:
    blacklist = file.read().split('\n')

for line in users.readlines():
    if len(line.rstrip()) < 3 or len(line.rstrip()) > 15:
        pass
    else:
        usernames.append(line.rstrip())

count = 0
def check(user):
    global count
    if len(user) > 15 or len(user) < 4:
        pass
    else:
        if user in blacklist:
            pass
        else:
            url = f"https://www.youtube.com/{user}"
            headers = {
                'X-Host': socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "fr,en-US;q=0.9,en;q=0.8",
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            }
            r1 = requests.get(url, headers=headers)
            if r1.status_code == 200:
                count += 1
                now = datetime.now()
                timestamp = now.strftime("%H:%M:%S")
                print(f'[{timestamp} | {count}]: {user} -> taken')
            if r1.status_code == 404:
                count += 1 
                now = datetime.now()
                timestamp = now.strftime("%H:%M:%S")
                print(f'[{timestamp} | {count}]: {user} -> avail')
                with open("avail.txt", "a") as file_object:
                    file_object.write(user + "\n")
                url = 'WEBHOOK URL GOES HERE'
                webhook = DiscordWebhook(url=url, content=f"Avail user: {user}")
                response = webhook.execute()

while True:
    threads = []
    for i in range(0, len(usernames)):
        t = threading.Thread(target=check, args=(usernames[i],), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.05)
    for x in threads:
        x.join()
