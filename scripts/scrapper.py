import os, yaml, json, hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup


cfg = yaml.safe_load(open("config.yaml"))


def fetch_rss(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "xml")
    articles = []
    for item in soup.find_all("item"):
        title = item.title.text
        link  = item.link.text
        content = requests.get(link).text
        articles.append({"title": title, "link": link, "content": content})
    return articles


def fetch_newsapi(key, query, language):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&language={language}&apiKey={key}"
    )
    data = requests.get(url).json()
    return [{"title": a["title"], "link": a["url"], "content": a.get("description","")} for a in data.get("articles",[])]


def save_articles(articles, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for art in articles:
        slug = hashlib.sha1(art["link"].encode()).hexdigest()[:8]
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fname = f"{timestamp}_{slug}.json"
        with open(os.path.join(output_dir, fname), "w", encoding="utf-8") as f:
            json.dump(art, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    out = cfg["output_dir"]
    
    for url in cfg["rss_feeds"]:
        save_articles(fetch_rss(url), out)
    
    ni = cfg["newsapi"]
    save_articles(fetch_newsapi(ni["key"], ni["query"], ni["language"]), out)
    print("✅ Raw data saved to", out)
