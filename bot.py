import os  
import json  
import asyncio  
from datetime import datetime, timedelta  
from telegram import Update  
from telegram.ext import Application, CommandHandler, ContextTypes  
from apscheduler.schedulers.asyncio import AsyncIOScheduler  

BOT_TOKEN = os.environ['BOT_TOKEN']  

# Load all posts (current + old)  
def load_posts():  
    try:  
        with open("posts.json", "r") as f:  
            current_posts = json.load(f)  
    except:  
        current_posts = {}  

    try:  
        with open("old_posts.json", "r") as f:  
            old_posts = json.load(f)  
    except:  
        old_posts = {}  

    return {**old_posts, **current_posts}  

# Auto-shift old posts weekly  
async def archive_old_posts():  
    try:  
        # Load current posts  
        with open("posts.json", "r") as f:  
            current_posts = json.load(f)  

        # Load old posts  
        try:  
            with open("old_posts.json", "r") as f:  
                old_posts = json.load(f)  
        except:  
            old_posts = {}  

        # Check dates  
        cutoff_date = datetime.now() - timedelta(days=7)  
        to_archive = {}  

        for post_id, post in list(current_posts.items()):  
            post_date = datetime.strptime(post["date"], "%Y-%m-%d")  
            if post_date < cutoff_date:  
                to_archive[post_id] = post  
                del current_posts[post_id]  

        # Update files  
        with open("posts.json", "w") as f:  
            json.dump(current_posts, f, indent=2)  

        with open("old_posts.json", "w") as f:  
            json.dump({**old_posts, **to_archive}, f, indent=2)  

    except Exception as e:  
        print(f"
