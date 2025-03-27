import requests
from bs4 import BeautifulSoup
from utils.common import normalize_text, general_crawl

CATEGORY_MAPPING = {
    "chinhtri": "Chính trị",
    "xahoi": "Xã hội",
    "phapluat": "Pháp luật",
    "kinhte": "Kinh tế",
    "thegioi": "Thế giới",
    "giaoduc": "Giáo dục",
    "yte_suckhoe": "Y tế - Sức khỏe",
    "vanhoa_giaitri": "Văn hóa - Giải trí",
    "nhipcau_bandoc": "Nhịp cầu bạn đọc",
    "khoahoc_congnghe": "Khoa học - Công nghệ"
}

CATEGORY_URLS = {
    "chinhtri": "https://www.sggp.org.vn/chinhtri/",
    "xahoi": "https://www.sggp.org.vn/xahoi/",
    "phapluat": "https://www.sggp.org.vn/phapluat/",
    "kinhte": "https://www.sggp.org.vn/kinhte/",
    "thegioi": "https://www.sggp.org.vn/thegioi/",
    "giaoduc": "https://www.sggp.org.vn/giaoduc/",
    "yte_suckhoe": "https://www.sggp.org.vn/yte-suckhoe/",
    "vanhoa_giaitri": "https://www.sggp.org.vn/vanhoa-giaitri/",
    "nhipcau_bandoc": "https://www.sggp.org.vn/nhipcau-bandoc/",
    "khoahoc_congnghe": "https://www.sggp.org.vn/khoahoc-congnghe/"
}

SELECTORS = {
    "article_links": "div.abf-cate a, div.zone-2 a"
}

def extract_sggp_article(url, expected_category, category_mapping):
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
            import time
            time.sleep(2)
    else:
        return None

    soup = BeautifulSoup(response.text, "lxml")
    title = soup.find("h1", class_="article_title cms-title")
    title = title.get_text(strip=True) if title else "Không có tiêu đề"

    author = soup.select_one("span.author.cms-source")
    author = author.get_text(strip=True) if author else "Không rõ tác giả"

    date = soup.select_one("time.time")
    date = date.get_text(strip=True) if date else "Không rõ ngày"

    category_element = soup.select_one("div.breadcrumbs a")
    category = category_element.get_text(strip=True) if category_element else "Không rõ thể loại"

    print(f"Đã lấy thể loại từ bài viết: {category} - {url}")

    normalized_category = normalize_text(category)
    normalized_expected = normalize_text(category_mapping.get(expected_category, expected_category))
    if normalized_category != normalized_expected:
        print(f"Bỏ qua bài viết '{title}' vì thể loại {category} không khớp với chuyên mục {expected_category}!")
        return None

    content_elements = soup.select("div.article_body.cms-body p")
    content = "\n".join([p.get_text(strip=True) for p in content_elements if p.get_text(strip=True)])

    return {
        "title": title,
        "author": author,
        "date": date,
        "category": category,
        "content": content,
        "url": url
    }

def crawl_sggp(n):
    return general_crawl(
        n=n,
        category_mapping=CATEGORY_MAPPING,
        category_urls=CATEGORY_URLS,
        site_prefix="https://www.sggp.org.vn",
        selectors=SELECTORS,
        extract_func=extract_sggp_article,
        table_name="sggp_articles"
    )
