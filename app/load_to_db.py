import os, json, yaml
from sqlalchemy import create_engine, text

# 설정 불러오기
cfg = yaml.safe_load(open("config.yaml"))
DB_URL = cfg.get("db_url", "postgresql://dataops:password123@localhost:5432/dataops")
RAW_DIR = cfg.get("output_dir", "data/raw")

engine = create_engine(DB_URL)

def load_raw_text():
    for fname in os.listdir(RAW_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(RAW_DIR, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        stmt = text("""
            INSERT INTO raw_text (title, link, content)
            VALUES (:title, :link, :content)
            ON CONFLICT (link) DO NOTHING
        """)
        engine.execute(stmt, {
            "title":   data.get("title", ""),
            "link":    data.get("link", ""),
            "content": data.get("content", "")
        })

if __name__ == "__main__":
    load_raw_text()
    print("✅ Loaded raw_text into database")
