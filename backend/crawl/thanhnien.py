import requests
from bs4 import BeautifulSoup
from database.database import save_articles_to_postgres
from utils.common import normalize_text
import time

# Ánh xạ chuyên mục URL với thể loại thực tế trên Thanh Niên
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

# Danh sách chuyên mục trên Thanh Niên
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

def get_articles_list(category_url, seen_urls, n):
    """Lấy danh sách bài viết từ box-top trước, nếu chưa đủ thì lấy từ list-listing-main"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print("Không thể truy cập danh mục.")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    articles = []

    # 🟢 Lấy bài từ box-top trước
    box_top_links = soup.select("div.box-category-item-main a.box-category-link-title")
    for link in box_top_links:
        title = link.get_text(strip=True)
        url = "https://thanhnien.vn" + link["href"]

        if url not in seen_urls:
            articles.append({"title": title, "url": url})
            seen_urls.add(url)

        if len(articles) >= n:  # Dừng ngay nếu đủ bài
            return articles

    # 🟢 Nếu chưa đủ bài, lấy thêm từ list-listing-flex
    if len(articles) < n:
        list_main_links = soup.select("div.list__stream-flex div.list__stream-main a.box-category-link-title")
        for link in list_main_links:
            title = link.get_text(strip=True)
            url = "https://thanhnien.vn" + link["href"]

            if url not in seen_urls:
                articles.append({"title": title, "url": url})
                seen_urls.add(url)

            if len(articles) >= n:  # Dừng ngay nếu đủ bài
                break

    return articles

def get_article_content(url, expected_category):
    """Lấy nội dung bài viết và kiểm tra thể loại có khớp với chuyên mục không"""
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
            time.sleep(2)  # Chờ 2 giây rồi thử lại lần nữa
    else:
        return None  # Nếu sau 3 lần vẫn lỗi thì bỏ bài này

    soup = BeautifulSoup(response.text, "lxml")

    # Lấy tiêu đề
    title = soup.find("h1", class_="detail-title").get_text(strip=True) if soup.find("h1", class_="detail-title") else "Không có tiêu đề"

    # Lấy tác giả
    author = soup.select_one("div.detail-author a.name").get_text(strip=True) if soup.select_one("div.detail-author a.name") else "Không rõ tác giả"

    # Lấy ngày đăng
    date = soup.select_one("div.detail-time").get_text(strip=True) if soup.select_one("div.detail-time") else "Không rõ ngày"

    # Lấy thể loại chính xác
    category_element = soup.select_one("div.detail-cate a")
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

    # Lấy nội dung bài viết
    content_elements = soup.select("div.detail-content[data-role='content'] p")
    content = "\n".join([p.get_text(strip=True) for p in content_elements if p.get_text(strip=True)])

    return {
        "title": title,
        "author": author,
        "date": date,
        "category": category,  # Trả về thể loại chính xác từ bài viết
        "content": content,
        "url": url
    }


def crawl_thanhnien(n):
    all_articles =[]

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
            print(f"Lưu {len(full_articles)} bài vào bảng thanhnien_articles (category: {category})")
            save_articles_to_postgres(full_articles, "thanhnien_articles", category)
            all_articles.extend(full_articles)
        else:
            print(f"Không có bài hợp lệ nào để lưu cho chuyên mục {category}.")

    return all_articles 

