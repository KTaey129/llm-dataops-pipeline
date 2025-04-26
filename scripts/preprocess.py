import os, json, yaml, re
from bs4 import BeautifulSoup
from langdetect import detect

# 설정 불러오기
cfg = yaml.safe_load(open("config.yaml"))
RAW_DIR   = cfg.get("output_dir", "data/raw")
CLEAN_DIR = cfg.get("clean_dir", "data/clean")

# HTML 태그 제거
def strip_html(text):
    return BeautifulSoup(text, "html.parser").get_text(separator=" ")

# 불필요 문자 제거
def normalize(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)         # 다중 공백 → 단일 공백
    text = re.sub(r"[^\w\d\s\.,;!?]", "", text)  # 알파벳/숫자/문장부호만
    return text.strip()

# 파일별 처리
def process_file(fname):
    with open(os.path.join(RAW_DIR, fname), encoding="utf-8") as f:
        data = json.load(f)
    content = data.get("content", "")
    text = strip_html(content)
    text = normalize(text)
    # 언어 감지 (영어/한국어/일본어만 통과 예시)
    try:
        lang = detect(text)
    except:
        return
    if lang not in ("en", "ko", "ja"):
        return
    out = {
        "title": data.get("title",""),
        "link":  data.get("link",""),
        "lang":  lang,
        "text":  text
    }
    # 클린 파일명
    os.makedirs(CLEAN_DIR, exist_ok=True)
    with open(os.path.join(CLEAN_DIR, fname), "w", encoding="utf-8") as wf:
        json.dump(out, wf, ensure_ascii=False, indent=2)

# 배치 처리
def main():
    for fname in os.listdir(RAW_DIR):
        if fname.endswith(".json"):
            process_file(fname)
    print("✅ Clean data saved to", CLEAN_DIR)

if __name__ == "__main__":
    main()
