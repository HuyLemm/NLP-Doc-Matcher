import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from database.database import save_articles_to_postgres
from utils.common import normalize_text
import time

# Ánh xạ chuyên mục URL với thể loại thực tế trên Tuổi Trẻ
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

# Danh sách chuyên mục trên Tuổi Trẻ
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


# def get_dynamic_html(url):
#     """Dùng Selenium để tải HTML sau khi JavaScript chạy"""
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")  # Chạy không hiển thị trình duyệt
#     options.add_argument("--disable-gpu")  
#     options.add_argument("--no-sandbox")  
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     driver.get(url)
#     time.sleep(5)  # Chờ trang tải xong

#     html = driver.page_source
#     driver.quit()
#     return html

# def get_articles_list(category_url, seen_urls, n):
#     """Lấy danh sách bài viết từ box-top trước, nếu chưa đủ thì lấy từ list__listing-main"""
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(category_url, headers=headers)
#     if response.status_code != 200:
#         print("Không thể truy cập danh mục.")
#         return []

#     soup = BeautifulSoup(response.text, "lxml")
#     articles = []

#     # 🟢 Lấy bài từ box-top trước
#     box_top_links = soup.select("div.box-top a.box-category-link-title")
#     for link in box_top_links:
#         title = link.get_text(strip=True)
#         url = "https://tuoitre.vn" + link["href"]

#         if url not in seen_urls:
#             articles.append({"title": title, "url": url})
#             seen_urls.add(url)

#         if len(articles) >= n:  # Dừng ngay nếu đủ bài
#             return articles

#     # Kiểm tra `list__listing-main` có bài không
#     list_main_links = soup.select("div.list__listing-main div.box-category-item div.box-content-title h3.box-title-text a.box-category-link-title")

#     # 🟢 Nếu đã có bài trong HTML, lấy luôn
#     if len(list_main_links) > 0:
#         print("✅ Dữ liệu có sẵn trong HTML, lấy bài viết từ `list__listing-main`...")
#     else:
#         print("⚠ Không tìm thấy bài viết trong HTML, tải lại bằng Selenium...")
#         html_content = get_dynamic_html(category_url)
#         soup = BeautifulSoup(html_content, "lxml")
#         list_main_links = soup.select("div.list__listing-main div.box-category-item div.box-content-title h3.box-title-text a.box-category-link-title")

#     # 🟢 Lấy bài từ `list__listing-main`
#     for link in list_main_links:
#         title = link.get_text(strip=True)
#         url = "https://tuoitre.vn" + link["href"]

#         if url not in seen_urls:
#             articles.append({"title": title, "url": url})
#             seen_urls.add(url)

#         if len(articles) >= n:  # Dừng ngay nếu đủ bài
#             break

#     return articles


def get_articles_list(category_url, seen_urls, n):
    """Lấy danh sách bài viết từ box-top trước, nếu chưa đủ thì lấy từ list-listing-main"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)
    if response.status_code != 200:
        print("Không thể truy cập danh mục.")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    articles = []

    # 🟢 Lấy bài từ box-top trước (ĐÃ ĐÚNG)
    box_top_links = soup.select("div.box-top a.box-category-link-title")
    for link in box_top_links:
        title = link.get_text(strip=True)
        url = "https://tuoitre.vn" + link["href"]

        if url not in seen_urls:
            articles.append({"title": title, "url": url})
            seen_urls.add(url)

        if len(articles) >= n:  # Dừng ngay nếu đủ bài
            return articles

    # 🟢 Nếu chưa đủ bài, lấy thêm từ list-listing-main (SỬA SELECTOR)
    if len(articles) < n:
        list_main_links = soup.select("div.list__listing-flex div.list__listing-sub a.box-category-link-title")
        for link in list_main_links:
            title = link.get_text(strip=True)
            url = "https://tuoitre.vn" + link["href"]

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

def crawl_tuoitre(n):
    all_articles = []

    for category, url in CATEGORY_URLS.items():
        print(f"\nĐang crawl {n} bài từ chuyên mục {category}...")

        full_articles = []
        seen_urls = set()
        ignored_articles = set()  
        attempts = 0  

        while len(full_articles) < n:
            print(f"\nThử lần {attempts + 1} để lấy đủ bài hợp lệ...")

            articles = get_articles_list(url, seen_urls, n)
            if not articles:
                print(f"Không tìm thấy thêm bài nào trong chuyên mục {category}. Dừng tìm kiếm.")
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
            print(f"Lưu {len(full_articles)} bài vào bảng tuoitre_articles (category: {category})")
            save_articles_to_postgres(full_articles, "tuoitre_articles", category)
            all_articles.extend(full_articles)
        else:
            print(f"Không có bài hợp lệ nào để lưu cho chuyên mục {category}.")
    return all_articles
