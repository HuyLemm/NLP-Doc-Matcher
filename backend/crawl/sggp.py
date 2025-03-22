import requests
from bs4 import BeautifulSoup
from database.database import save_articles_to_postgres
from utils.common import normalize_text
import time

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

def get_articles_list(category_url, seen_urls, n):
    """Lấy danh sách bài viết từ `abf-cate`, nếu chưa đủ thì lấy từ `zone-2`."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print("❌ Không thể truy cập danh mục.")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    articles = []

    # 🟢 Lấy bài từ `abf-cate`
    box_top_links = soup.select("div.abf-cate a")
    for link in box_top_links:
        title = link.get_text(strip=True)
        url = "https://www.sggp.org.vn" + link["href"]

        if url not in seen_urls:
            articles.append({"title": title, "url": url})
            seen_urls.add(url)

        if len(articles) >= n:
            return articles

    # 🔎 Nếu chưa đủ bài, lấy từ `zone-2`
    list_main_links = soup.select("div.zone-2 a")
    for link in list_main_links:
        title = link.get_text(strip=True)
        url = "https://www.sggp.org.vn" + link["href"]

        if url not in seen_urls:
            articles.append({"title": title, "url": url})
            seen_urls.add(url)

        if len(articles) >= n:
            break

    return articles

def get_article_content(url, expected_category):
    """Lấy nội dung bài viết từ báo Sài Gòn Giải Phóng và kiểm tra thể loại"""
    headers = {"User-Agent": "Mozilla/5.0"}

    # Thử lại 3 lần nếu gặp lỗi kết nối
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Không thể tải bài viết: {url}")
                return None
            break
        except requests.exceptions.RequestException:
            print(f"Kết nối bị lỗi, thử lại lần {attempt+1}...")
            time.sleep(2)
    else:
        return None

    soup = BeautifulSoup(response.text, "lxml")

    # 🟢 Lấy thể loại bài viết (Ảnh 2)
    category_element = soup.select_one("div.breadcrumbs a")
    category = category_element.get_text(strip=True) if category_element else "Không rõ thể loại"

    # 🟢 Lấy tiêu đề bài viết (Ảnh 3)
    title = soup.find("h1", class_="article_title cms-title")
    title = title.get_text(strip=True) if title else "Không có tiêu đề"

    # 🟢 Lấy tác giả & thời gian (Ảnh 4)
    author = soup.select_one("span.author.cms-source")
    author = author.get_text(strip=True) if author else "Không rõ tác giả"

    date = soup.select_one("time.time")
    date = date.get_text(strip=True) if date else "Không rõ ngày"

    # Debug: In thể loại để kiểm tra
    print(f"Đã lấy thể loại từ bài viết: {category} - {url}")

    # Chuẩn hóa thể loại trước khi so sánh
    normalized_category = normalize_text(category)
    normalized_expected = normalize_text(CATEGORY_MAPPING.get(expected_category, expected_category))

    # Nếu thể loại không khớp chuyên mục => BỎ QUA
    if normalized_category != normalized_expected:
        print(f"Bỏ qua bài viết '{title}' vì thể loại {category} không khớp với chuyên mục {expected_category}!")
        return None

    # 🟢 Lấy nội dung bài viết (Ảnh 5)
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
    for category, url in CATEGORY_URLS.items():
        print(f"\nĐang crawl {n} bài từ chuyên mục {category}...")

        full_articles = []
        seen_urls = set()
        ignored_articles = set()  
        attempts = 0  

        while len(full_articles) < n:
            print(f"\n🔄 Thử lần {attempts + 1} để lấy đủ bài hợp lệ...")

            articles = get_articles_list(url, seen_urls, n)
            if not articles:
                print(f"⚠ Không tìm thấy thêm bài nào trong chuyên mục {category}. Dừng tìm kiếm.")
                break

            for article in articles:
                if article["url"] in ignored_articles:
                    continue  

                content = get_article_content(article["url"], category) 
                if content:
                    print(f"Lưu bài viết: {content['title']} - Thể loại: {content['category']}")
                    full_articles.append(content)
                    if len(full_articles) >= n:
                        break  
                else:
                    ignored_articles.add(article["url"])  

            attempts += 1
            if len(full_articles) < n:
                print(f"Chưa đủ bài hợp lệ ({len(full_articles)}/{n}), tiếp tục tìm kiếm...")
            else:
                break  

        if full_articles:
            print(f"Lưu {len(full_articles)} bài vào bảng sggp_articles (category: {category})")
            save_articles_to_postgres(full_articles, "sggp_articles", category)
            return full_articles
        else:
            print(f"Không có bài hợp lệ nào để lưu cho chuyên mục {category}.")
