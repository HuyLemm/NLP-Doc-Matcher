import requests
from bs4 import BeautifulSoup
from database.database import save_articles_to_postgres
from utils.common import normalize_text
import time

# Ánh xạ chuyên mục URL với thể loại thực tế trên Báo Người Lao Động
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

# Danh sách chuyên mục trên Báo Người Lao Động
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



def get_articles_list(category_url, seen_urls, n):
    """Lấy danh sách bài viết từ box-category-middle trước, nếu chưa đủ thì lấy từ list__news-flex"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print("❌ Không thể truy cập danh mục.")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    articles = []

    # 🟢 Lấy bài từ `box-category-middle` trước
    box_top_links = soup.select("div.box-category-middle a.box-category-link-title")
    for link in box_top_links:
        title = link.get_text(strip=True)
        url = "https://nld.com.vn" + link["href"]

        if url not in seen_urls:
            articles.append({"title": title, "url": url})
            seen_urls.add(url)

        if len(articles) >= n:  # Dừng ngay nếu đủ bài
            return articles

    # 🔎 Nếu chưa đủ bài, lấy từ `list__news-flex`
    list_main_links = soup.select("div.list__news-flex div.list__news-item a.box-category-link-title")

    for link in list_main_links:
        title = link.get_text(strip=True)
        url = "https://nld.com.vn" + link["href"]

        if url not in seen_urls:
            articles.append({"title": title, "url": url})
            seen_urls.add(url)

        if len(articles) >= n:  # Dừng ngay nếu đủ bài
            break

    return articles


def get_article_content(url, expected_category):
    """Lấy nội dung bài viết từ báo Người Lao Động và kiểm tra thể loại"""
    headers = {"User-Agent": "Mozilla/5.0"}

    # Thử lại 3 lần nếu gặp lỗi kết nối
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Không thể tải bài viết: {url}")
                return None
            break  # Nếu tải thành công thì thoát vòng lặp
        except requests.exceptions.RequestException:
            print(f"Kết nối bị lỗi, thử lại lần {attempt+1}...")
            time.sleep(2)
    else:
        return None  # Nếu sau 3 lần vẫn lỗi thì bỏ bài này

    soup = BeautifulSoup(response.text, "lxml")

    # 🟢 Lấy tiêu đề bài viết (Ảnh 5)
    title = soup.find("h1", class_="detail-title")
    title = title.get_text(strip=True) if title else "Không có tiêu đề"

    # 🟢 Lấy tác giả (Ảnh 2)
    author = soup.select_one("div.detail-author p.name[data-role='author']")
    author = author.get_text(strip=True) if author else "Không rõ tác giả"

    # 🟢 Lấy ngày đăng bài viết (Ảnh 3)
    date = soup.select_one("div.detail-time div[data-role='publishdate']")
    date = date.get_text(strip=True) if date else "Không rõ ngày"

    # 🟢 Lấy thể loại bài viết (Ảnh 1)
    category_element = soup.select_one("div.detail-cate a.category-name_ac")
    category = category_element.get_text(strip=True) if category_element else "Không rõ thể loại"

    # Debug: In thể loại để kiểm tra
    print(f"Đã lấy thể loại từ bài viết: {category} - {url}")

    # Chuẩn hóa thể loại trước khi so sánh
    normalized_category = normalize_text(category)
    normalized_expected = normalize_text(CATEGORY_MAPPING.get(expected_category, expected_category))

    # Nếu thể loại không khớp chuyên mục => BỎ QUA
    if normalized_category != normalized_expected:
        print(f"Bỏ qua bài viết '{title}' vì thể loại {category} không khớp với chuyên mục {expected_category}!")
        return None

    # 🟢 Lấy nội dung bài viết (Ảnh 4)
    content_elements = soup.select("div.detail-content.afcbc-body[data-role='content'] p")
    content = "\n".join([p.get_text(strip=True) for p in content_elements if p.get_text(strip=True)])

    return {
        "title": title,
        "author": author,
        "date": date,
        "category": category,  # Trả về thể loại chính xác từ bài viết
        "content": content,
        "url": url
    }

def crawl_nld(n):
    all_articles = []

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
            print(f"Lưu {len(full_articles)} bài vào bảng nld_articles (category: {category})")
            save_articles_to_postgres(full_articles, "nld_articles", category)
            all_articles.extend(full_articles)  # ✅ Gộp vào tổng
        else:
            print(f"Không có bài hợp lệ nào để lưu cho chuyên mục {category}.")

    return all_articles  # ✅ Trả về toàn bộ bài đã lưu


