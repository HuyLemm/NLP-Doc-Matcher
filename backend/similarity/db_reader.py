from utils.config import DB_CONFIG
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.common import clean_text

def fetch_all_contents():
    all_data = []

    for table, source_name in [
        ("tuoitre_articles", "Tuổi Trẻ"),
        ("thanhnien_articles", "Thanh Niên"),
        ("nld_articles", "Người Lao Động"),
        ("business_data", "Business Documents"),
    ]:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if table == "business_data":
                cursor.execute("SELECT file_name, file_type, content, source FROM business_data")
                rows = cursor.fetchall()
                for row in rows:
                    text = row[2] or ""
                    if text.strip():
                        all_data.append({
                            "source": source_name,
                            "category": row[3] or "Không rõ",
                            "text": text
                        })
            else:
                cursor.execute(f"SELECT title, author, date, content, url, category FROM {table}")
                rows = cursor.fetchall()
                for row in rows:
                    text = row[3] or ""
                    if text.strip():
                        all_data.append({
                            "source": source_name,
                            "category": row[5] or "Không rõ",
                            "text": text
                        })
        except Exception as e:
            print(f"Lỗi khi đọc bảng {table}: {e}")
        finally:
            cursor.close()
            conn.close()

    return all_data
