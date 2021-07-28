import sys
import os
import requests
import random

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from app import db
from models import *

forums_seed = {
    "The Original Trilogy":"Talk about the movies that started it all!",
    "The Prequels":"Maybe they weren't great, but they sure are fun to talk about!",
    "The Disney Sequels":"Abandon all hope, ye who enter here!",
    "TV Shows and Specials":"The Mandalorian, The Clone Wars, etc.",
    "Games":"Chat about your favorite games!",
    "Off-Topic":"Best not mentioned elsewhere"
}

content = []
content.append(requests.get(f'http://loripsum.net/api/1/short/plaintext').text)
content.append(requests.get(f'http://loripsum.net/api/2/short/plaintext').text)
content.append(requests.get(f'http://loripsum.net/api/3/short/plaintext').text)
content.append(requests.get(f'http://loripsum.net/api/1/medium/plaintext').text)

print("Requested test content...")

print("Seeding database with test data...")

for forum in forums_seed:
    new_forum = Forum(forum, forums_seed[forum])
    db.session.add(new_forum)
db.session.commit()
print("    created forums...")

res = requests.get('https://randomuser.me/api/?results=100')
users_seed = res.json()["results"]
for user in users_seed:
    new_user = User(user["login"]["username"],user["email"],user["login"]["password"])
    db.session.add(new_user)
db.session.commit()
print("    created users...")

forums = Forum.query.all()
thread_count = 0
post_count = 0
for forum in forums:
    for i in range(random.randint(50,100)):
        thread_count += 1
        new_title = f'Test Thread #{thread_count}'
        op = random.randint(1,100)
        op_content = content[random.randint(0,len(content)-1)]
        new_thread = Thread(forum.id, new_title, op, op_content)
        db.session.add(new_thread)
        db.session.commit()
        for j in range(random.randint(0,50)):
            poster = random.randint(1,100)
            post_content = content[random.randint(0,len(content)-1)]
            new_post = Post(new_thread.id, poster, post_content)
            db.session.add(new_post)
            post_count += 1
            new_thread.last_reply = new_post.created_at
            db.session.commit()

print("    created threads and posts...")
print(f"        Threads created: {thread_count}")
print(f"        Posts created: {post_count}")

