import requests
from bs4 import BeautifulSoup
from utils.common import normalize_text, general_crawl
import time

CATEGORY_MAPPING = {
    "chinhtri": "Chính trị",
    "thoisu": "Thời sự",
    "thegioi": "Thế giới",
    "kinhte": "Kinh tế",
    "doisong": "Đời sống",
    "suckhoe": "Sức khỏe",
    "gioitre": "Giới trẻ",
    "giaoduc": "Giáo dục",
    "dulich": "Du lịch",
    "vanhoa": "Văn hóa",
    "giaitri": "Giải trí",
    "thethao": "Thể thao",
    "congnghe": "Công nghệ",
    "xe": "Xe",
}

CATEGORY_URLS = {
    "chinhtri": "https://thanhnien.vn/chinh-tri.htm",
    "thoisu": "https://thanhnien.vn/thoi-su.htm",
    "thegioi": "https://thanhnien.vn/the-gioi.htm",
    "kinhte": "https://thanhnien.vn/kinh-te.htm",
    "doisong": "https://thanhnien.vn/doi-song.htm",
    "suckhoe": "https://thanhnien.vn/suc-khoe.htm",
    "gioitre": "https://thanhnien.vn/gioi-tre.htm",
    "giaoduc": "https://thanhnien.vn/giao-duc.htm",
    "dulich": "https://thanhnien.vn/du-lich.htm",
    "vanhoa": "https://thanhnien.vn/van-hoa.htm",
    "giaitri": "https://thanhnien.vn/giai-tri.htm",
    "thethao": "https://thanhnien.vn/the-thao.htm",
    "congnghe": "https://thanhnien.vn/cong-nghe.htm",
    "xe": "https://thanhnien.vn/xe.htm",
}

SELECTORS = {
    "article_links": "div.box-category-item-main a.box-category-link-title, div.list__stream-flex div.list__stream-main a.box-category-link-title"
}

def extract_thanhnien_article(url, expected_category, category_mapping):
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

    author = soup.select_one("div.detail-author a.name")
    author = author.get_text(strip=True) if author else "Không rõ tác giả"

    date = soup.select_one("div.detail-time")
    date = date.get_text(strip=True) if date else "Không rõ ngày"

    category_element = soup.select_one("div.detail-cate a")
    category = category_element.get_text(strip=True) if category_element else "Không rõ thể loại"

    print(f"Đã lấy thể loại từ bài viết: {category} - {url}")

    normalized_category = normalize_text(category)
    normalized_expected = normalize_text(category_mapping.get(expected_category, expected_category))
    if normalized_category != normalized_expected:
        print(f"Bỏ qua bài viết '{title}' vì thể loại {category} không khớp với chuyên mục {expected_category}!")
        return None

    content_elements = soup.select("div.detail-content[data-role='content'] p")
    content = "\n".join([p.get_text(strip=True) for p in content_elements if p.get_text(strip=True)])

    return {
        "title": title,
        "author": author,
        "date": date,
        "category": category,
        "content": content,
        "url": url
    }

def crawl_thanhnien(n):
    return general_crawl(
        n=n,
        category_mapping=CATEGORY_MAPPING,
        category_urls=CATEGORY_URLS,
        site_prefix="https://thanhnien.vn",
        selectors=SELECTORS,
        extract_func=extract_thanhnien_article,
        table_name="thanhnien_articles"
    )
