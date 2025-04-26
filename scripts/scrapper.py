import os, yaml, json, hashlib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    try:
        with open("config.yaml", "r", encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config.yaml: {e}")
        raise

def fetch_rss(url):
    try:
        logger.info(f"Fetching RSS feed from: {url}")
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "xml")
        articles = []
        
        for item in soup.find_all("item"):
            try:
                title = item.title.text.strip()
                link = item.link.text.strip()
                pub_date = item.pubDate.text if item.pubDate else datetime.utcnow().isoformat()
                
                # Fetch article content
                content_res = requests.get(link, timeout=10)
                content_res.raise_for_status()
                content_soup = BeautifulSoup(content_res.text, 'html.parser')
                
                # Extract main content (adjust selector based on YTN's HTML structure)
                content = content_soup.find('div', class_='article_body').get_text(strip=True) if content_soup.find('div', class_='article_body') else ""
                
                articles.append({
                    "title": title,
                    "link": link,
                    "content": content,
                    "published_date": pub_date,
                    "source": "YTN"
                })
                logger.info(f"Successfully processed article: {title}")
            except Exception as e:
                logger.error(f"Error processing article: {e}")
                continue
                
        return articles
    except Exception as e:
        logger.error(f"Error fetching RSS feed: {e}")
        return []

def fetch_newsapi(key, query, language):
    if not key:
        logger.warning("NewsAPI key not provided, skipping NewsAPI fetch")
        return []
        
    try:
        logger.info(f"Fetching news from NewsAPI with query: {query}")
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&language={language}&apiKey={key}"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article["title"],
                "link": article["url"],
                "content": article.get("description", ""),
                "published_date": article.get("publishedAt", ""),
                "source": "NewsAPI"
            })
        return articles
    except Exception as e:
        logger.error(f"Error fetching from NewsAPI: {e}")
        return []

def save_articles(articles, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        for art in articles:
            slug = hashlib.sha1(art["link"].encode()).hexdigest()[:8]
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            fname = f"{timestamp}_{slug}.json"
            filepath = os.path.join(output_dir, fname)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(art, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved article to: {filepath}")
    except Exception as e:
        logger.error(f"Error saving articles: {e}")

if __name__ == "__main__":
    try:
        cfg = load_config()
        out = cfg["output_dir"]
        
        # Fetch from YTN RSS
        for url in cfg["rss_feeds"]:
            articles = fetch_rss(url)
            save_articles(articles, out)
        
        # Fetch from NewsAPI
        ni = cfg["newsapi"]
        articles = fetch_newsapi(ni["key"], ni["query"], ni["language"])
        save_articles(articles, out)
        
        logger.info(f"✅ Raw data saved to {out}")
    except Exception as e:
        logger.error(f"Main execution error: {e}")
