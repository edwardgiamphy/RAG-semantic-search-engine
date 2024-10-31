"""get the RSS of public website"""

import feedparser
import json

url = "https://www.public.fr/people/feed"
url = "https://vsd.fr/actu-people/feed/"

feed = feedparser.parse(url)

articles = []

for entry in feed.entries:
    articles.append({
        "title": entry.title,
        "summary": entry.summary,
        "content": entry.get("content", [{}])[0].get("value", "")
    })

with open("articles2.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

