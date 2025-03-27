import unicodedata
import requests
from bs4 import BeautifulSoup
import time
from database.database import save_articles_to_postgres
import re

def normalize_text(text):
    """
    Chuẩn hóa văn bản:
    - Xóa dấu tiếng Việt
    - Chuyển về chữ thường
    - Loại bỏ khoảng trắng thừa
    """
    if not isinstance(text, str):
        return ""

    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = normalized.encode('ASCII', 'ignore').decode('utf-8')
    return " ".join(ascii_text.lower().split())

def clean_text(text: str) -> str:
    """
    Làm sạch văn bản: xoá ký tự đặc biệt, chuẩn hóa unicode, xóa dấu, viết thường.
    """
    if not text:
        return ""

    # Chuẩn hoá unicode
    text = unicodedata.normalize('NFKC', text)

    # Xoá dấu câu, ký tự đặc biệt
    text = re.sub(r"[^\w\s]", " ", text)

    # Xoá số
    text = re.sub(r"\d+", " ", text)

    # Xoá nhiều khoảng trắng
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def general_crawl(n, category_mapping, category_urls, site_prefix, selectors, extract_func, table_name):
    all_articles = []

    for category, url in category_urls.items():
        print(f"\nĐang crawl {n} bài từ chuyên mục {category}...")

        full_articles = []
        seen_urls = set()
        ignored_urls = set()
        attempts = 0

        while len(full_articles) < n:
            print(f"\n🔄 Thử lần {attempts + 1} để lấy đủ bài hợp lệ...")

            try:
                res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if res.status_code != 200:
                    print("❌ Không thể truy cập danh mục.")
                    break
                soup = BeautifulSoup(res.text, "lxml")
                article_links = soup.select(selectors['article_links'])

                articles = []
                for link in article_links:
                    title = link.get_text(strip=True)
                    full_url = site_prefix + link['href']
                    if full_url not in seen_urls:
                        articles.append({"title": title, "url": full_url})
                        seen_urls.add(full_url)
                    if len(articles) >= n:
                        break
            except Exception as e:
                print(f"❌ Lỗi khi lấy danh sách bài: {e}")
                break

            if not articles:
                print(f"⚠ Không tìm thấy bài nào trong chuyên mục {category}.")
                break

            for article in articles:
                if article["url"] in ignored_urls:
                    continue

                content = extract_func(article["url"], category, category_mapping)
                if content:
                    full_articles.append(content)
                    if len(full_articles) >= n:
                        break
                else:
                    ignored_urls.add(article["url"])

            attempts += 1

        if full_articles:
            print(f"Lưu {len(full_articles)} bài vào bảng {table_name} (category: {category})")
            save_articles_to_postgres(full_articles, table_name, category)
            all_articles.extend(full_articles)
        else:
            print(f"Không có bài hợp lệ nào để lưu cho chuyên mục {category}.")

    return all_articles
