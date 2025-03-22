import threading
from crawl.nld import crawl_nld
from crawl.sggp import crawl_sggp
from crawl.thanhnien import crawl_thanhnien
from crawl.tuoitre import crawl_tuoitre
from database.database import save_articles_to_postgres

# Ánh xạ nguồn báo với script tương ứng
NEWS_SOURCES = {
    "tuoitre": crawl_tuoitre,
    "thanhnien": crawl_thanhnien,
    "nld": crawl_nld,
    "sggp": crawl_sggp
}

def crawl_news(source, num_articles):
    if source not in NEWS_SOURCES:
        print(f"❌ Báo '{source}' không được hỗ trợ.")
        return []

    print(f"🔍 Đang crawl {num_articles} bài từ {source}...")
    articles = NEWS_SOURCES[source](num_articles)

    if articles:
        save_articles_to_postgres(articles, f"{source}_articles", source)
        print(f"✅ Đã lưu {len(articles)} bài vào PostgreSQL.")
    else:
        print(f"⚠ Không có bài viết nào được crawl từ {source}.")

    return articles  # ✅ TRẢ VỀ KẾT QUẢ


def start_crawling(sources, num_articles):
    all_articles = []

    def threaded_crawl(src):
        articles = crawl_news(src, num_articles)
        if articles:
            all_articles.extend(articles)

    threads = [threading.Thread(target=threaded_crawl, args=(src,)) for src in sources]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return all_articles


