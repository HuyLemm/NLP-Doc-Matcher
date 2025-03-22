import psycopg2
from psycopg2.extras import execute_values

# Hàm kết nối PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname="text_similarity",
        user="postgres",
        password="alvinyeupaoi1711",  # Thay bằng mật khẩu thực tế
        host="localhost",
        port="5432"
    )

# Hàm lưu bài viết vào PostgreSQL (đã có)
def save_articles_to_postgres(articles, table_name, category):
    if not articles:
        print(f"⚠ Không có bài viết nào từ chuyên mục {category} để lưu.")
        return

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        title TEXT,
        author TEXT,
        date TEXT,
        content TEXT,
        url TEXT UNIQUE,
        category TEXT
    );
    """

    insert_query = f"""
    INSERT INTO {table_name} (title, author, date, content, url, category)
    VALUES %s
    ON CONFLICT (url) DO NOTHING;
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()

        values = [(art["title"], art["author"], art["date"], art["content"], art["url"], category) for art in articles]
        execute_values(cursor, insert_query, values)
        conn.commit()

        print(f"Lưu {len(articles)} bài vào bảng {table_name} (category: {category}) thành công!")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu vào PostgreSQL: {e}")
    finally:
        cursor.close()
        conn.close()

# 🟢 Mới: Hàm lưu tài liệu PDF, Word, Excel vào PostgreSQL
def save_documents_to_postgres(documents):
    if not documents:
        print(f"⚠ Không có tài liệu nào để lưu vào PostgreSQL.")
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        file_name VARCHAR(255),
        file_type VARCHAR(50),
        content TEXT,
        extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source VARCHAR(255)
    );
    """

    insert_query = """
    INSERT INTO documents (file_name, file_type, content, source)
    VALUES %s
    ON CONFLICT (file_name) DO NOTHING;
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()

        values = [(doc["file_name"], doc["file_type"], doc["content"], doc["source"]) for doc in documents]
        execute_values(cursor, insert_query, values)
        conn.commit()

        print(f"✅ Đã lưu {len(documents)} tài liệu vào PostgreSQL!")
    except Exception as e:
        print(f"❌ Lỗi khi lưu tài liệu vào PostgreSQL: {e}")
    finally:
        cursor.close()
        conn.close()
