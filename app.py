#!/usr/bin/env python3
"""
Reddit Personal Assistant (read-only starter)

What it does:
- Auth with Reddit OAuth (script app)
- Reads "hot" posts from selected subreddits
- Optional keyword filtering
- Prints concise summaries

Setup:
1) pip install praw python-dotenv
2) Create .env in same folder:
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USERNAME=...
REDDIT_PASSWORD=...
REDDIT_USER_AGENT=reddit-personal-assistant/0.1 by u/yourusername
3) python app.py
"""

import os
from datetime import datetime, timezone
from typing import List
import praw
from dotenv import load_dotenv

# ---------- Config ----------
SUBREDDITS = ["india", "technology", "worldnews", "Cricket"]
KEYWORDS = ["ai", "open source", "india", "t20", "cricket"] # set [] to disable filtering
POST_LIMIT_PER_SUB = 10
# ---------------------------


def load_config():
load_dotenv()
required = [
"REDDIT_CLIENT_ID",
"REDDIT_CLIENT_SECRET",
"REDDIT_USERNAME",
"REDDIT_PASSWORD",
"REDDIT_USER_AGENT",
]
missing = [k for k in required if not os.getenv(k)]
if missing:
raise ValueError(f"Missing env vars: {', '.join(missing)}")


def create_reddit():
return praw.Reddit(
client_id=os.environ["REDDIT_CLIENT_ID"],
client_secret=os.environ["REDDIT_CLIENT_SECRET"],
username=os.environ["REDDIT_USERNAME"],
password=os.environ["REDDIT_PASSWORD"],
user_agent=os.environ["REDDIT_USER_AGENT"],
)


def matches_keywords(text: str, keywords: List[str]) -> bool:
if not keywords:
return True
t = (text or "").lower()
return any(k.lower() in t for k in keywords)


def short(s: str, n: int = 140) -> str:
s = (s or "").replace("\n", " ").strip()
return s if len(s) <= n else s[: n - 1] + "…"


def summarize_submission(sub):
created = datetime.fromtimestamp(sub.created_utc, tz=timezone.utc).astimezone()
return (
f"- r/{sub.subreddit.display_name} | {short(sub.title, 100)}\n"
f" 👍 {sub.score} 💬 {sub.num_comments} "
f"🕒 {created.strftime('%Y-%m-%d %H:%M %Z')}\n"
f" 🔗 https://reddit.com{sub.permalink}"
)


def main():
load_config()
reddit = create_reddit()

print("Fetching posts...\n")
total = 0

for sub_name in SUBREDDITS:
subreddit = reddit.subreddit(sub_name)
print(f"## r/{sub_name}")
shown = 0

for post in subreddit.hot(limit=POST_LIMIT_PER_SUB):
haystack = f"{post.title}\n{getattr(post, 'selftext', '')}"
if not matches_keywords(haystack, KEYWORDS):
continue

print(summarize_submission(post))
shown += 1
total += 1

if shown == 0:
print("- No matching posts found.")
print()

print(f"Done. Total matched posts: {total}")


if __name__ == "__main__":
main()
