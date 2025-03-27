import requests
from bs4 import BeautifulSoup
from utils.common import normalize_text, general_crawl

CATEGORY_MAPPING = {
    "thoisu": "Thời sự",
    "thegioi": "Thế giới",
    "phapluat": "Pháp luật",
    "kinhdoanh": "Kinh doanh",
    "congnghe": "Công nghệ",
    "xe": "Xe",
    "dulich": "Du lịch",
    "nhipsongtre": "Nhịp sống trẻ",
    "vanhoa": "Văn hóa",
    "giaitri": "Giải trí",
    "thethao": "Thể thao",
    "giaoduc": "Giáo dục",
    "nhadat": "Nhà đất",
    "suckhoe": "Sức khỏe",
    "giathat": "Giả - Thật",
    "bandoc": "Bạn đọc làm báo"
}

CATEGORY_URLS = {
    "thoisu": "https://tuoitre.vn/thoi-su.htm",
    "thegioi": "https://tuoitre.vn/the-gioi.htm",
    "phapluat": "https://tuoitre.vn/phap-luat.htm",
    "kinhdoanh": "https://tuoitre.vn/kinh-doanh.htm",
    "congnghe": "https://tuoitre.vn/cong-nghe.htm",
    "xe": "https://tuoitre.vn/xe.htm",
    "dulich": "https://tuoitre.vn/du-lich.htm",
    "nhipsongtre": "https://tuoitre.vn/nhip-song-tre.htm",
    "vanhoa": "https://tuoitre.vn/van-hoa.htm",
    "giaitri": "https://tuoitre.vn/giai-tri.htm",
    "thethao": "https://tuoitre.vn/the-thao.htm",
    "giaoduc": "https://tuoitre.vn/giao-duc.htm",
    "nhadat": "https://tuoitre.vn/nha-dat.htm",
    "suckhoe": "https://tuoitre.vn/suc-khoe.htm",
    "giathat": "https://tuoitre.vn/gia-that.htm",
    "bandoc": "https://tuoitre.vn/ban-doc-lam-bao.htm"
}

SELECTORS = {
    "article_links": "div.box-top a.box-category-link-title, div.list__listing-flex div.list__listing-sub a.box-category-link-title"
}

def extract_tuoitre_article(url, expected_category, category_mapping):
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

def crawl_tuoitre(n):
    return general_crawl(
        n=n,
        category_mapping=CATEGORY_MAPPING,
        category_urls=CATEGORY_URLS,
        site_prefix="https://tuoitre.vn",
        selectors=SELECTORS,
        extract_func=extract_tuoitre_article,
        table_name="tuoitre_articles"
    )
