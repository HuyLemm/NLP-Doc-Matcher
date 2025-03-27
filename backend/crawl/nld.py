from utils.common import normalize_text, general_crawl
import requests
from bs4 import BeautifulSoup

# Các cấu hình riêng cho báo Người Lao Động
CATEGORY_MAPPING = {
    "thoisu": "Thời sự",
    "quocte": "Quốc tế",
    "laodong": "Lao động",
    "bandoc": "Bạn đọc",
    "netzero": "Net Zero",
    "kinhte": "Kinh tế",
    "suckhoe": "Sức khỏe",
    "giaoduc": "Giáo dục",
    "phapluat": "Pháp luật",
    "vanhoa_vannghe": "Văn hóa - Văn nghệ",
    "giaitri": "Giải trí",
    "thethao": "Thể thao",
    "ai365": "AI 365",
    "giadinh": "Gia đình"
}

CATEGORY_URLS = {
    "thoisu": "https://nld.com.vn/thoi-su.htm",
    "quocte": "https://nld.com.vn/quoc-te.htm",
    "laodong": "https://nld.com.vn/lao-dong.htm",
    "bandoc": "https://nld.com.vn/ban-doc.htm",
    "netzero": "https://nld.com.vn/net-zero.htm",
    "kinhte": "https://nld.com.vn/kinh-te.htm",
    "suckhoe": "https://nld.com.vn/suc-khoe.htm",
    "giaoduc": "https://nld.com.vn/giao-duc-khoa-hoc.htm",
    "phapluat": "https://nld.com.vn/phap-luat.htm",
    "vanhoa_vannghe": "https://nld.com.vn/van-hoa-van-nghe.htm",
    "giaitri": "https://nld.com.vn/giai-tri.htm",
    "thethao": "https://nld.com.vn/the-thao.htm",
    "ai365": "https://nld.com.vn/ai-365.htm",
    "giadinh": "https://nld.com.vn/gia-dinh.htm"
}

SELECTORS = {
    "article_links": "div.box-category-middle a.box-category-link-title, div.list__news-flex a.box-category-link-title"
}

def extract_nld_article(url, expected_category, category_mapping):
    headers = {"User-Agent": "Mozilla/5.0"}
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Không thể tải bài viết: {url}")
                return None
            break
        except requests.exceptions.RequestException:
            print(f"Kết nối bị lỗi, thử lại lần {attempt + 1}...")
            time.sleep(2)
    else:
        return None

    soup = BeautifulSoup(response.text, "lxml")

    title = soup.find("h1", class_="detail-title")
    title = title.get_text(strip=True) if title else "Không có tiêu đề"

    author = soup.select_one("div.detail-author p.name[data-role='author']")
    author = author.get_text(strip=True) if author else "Không rõ tác giả"

    date = soup.select_one("div.detail-time div[data-role='publishdate']")
    date = date.get_text(strip=True) if date else "Không rõ ngày"

    category_element = soup.select_one("div.detail-cate a.category-name_ac")
    category = category_element.get_text(strip=True) if category_element else "Không rõ thể loại"

    print(f"Đã lấy thể loại từ bài viết: {category} - {url}")

    if normalize_text(category) != normalize_text(category_mapping.get(expected_category, expected_category)):
        print(f"Bỏ qua bài viết '{title}' vì thể loại {category} không khớp với chuyên mục {expected_category}")
        return None

    content_elements = soup.select("div.detail-content.afcbc-body[data-role='content'] p")
    content = "\n".join(p.get_text(strip=True) for p in content_elements if p.get_text(strip=True))

    return {
        "title": title,
        "author": author,
        "date": date,
        "category": category,
        "content": content,
        "url": url
    }

def crawl_nld(n):
    return general_crawl(
        n=n,
        category_mapping=CATEGORY_MAPPING,
        category_urls=CATEGORY_URLS,
        site_prefix="https://nld.com.vn",
        selectors=SELECTORS,
        extract_func=extract_nld_article,
        table_name="nld_articles"
    )
