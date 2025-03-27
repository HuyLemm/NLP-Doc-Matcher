# similarity/compare_uploaded.py

from utils.common import clean_text
from similarity.db_reader import fetch_all_contents
from similarity.vectorizer import get_vectorizer_and_vectors, vectorize_new_text
from similarity.similarity_calculator import calculate_similarities


def compare_uploaded_document(uploaded_text, top_k=5):
    """
    So sánh văn bản upload với toàn bộ kho văn bản đã lưu trong PostgreSQL.
    Trả về danh sách các văn bản giống nhất.
    """
    if not uploaded_text.strip():
        return []

    # 1. Làm sạch văn bản upload
    cleaned_text = clean_text(uploaded_text)

    # 2. Lấy toàn bộ văn bản trong DB (đã làm sạch)
    corpus = fetch_all_contents()
    if not corpus:
        return []

    # 3. Ghép văn bản thành danh sách để vector hóa
    all_texts = [doc["text"] for doc in corpus]

    # 4. Vector hóa toàn bộ corpus và văn bản upload
    vectorizer, corpus_vectors = get_vectorizer_and_vectors(all_texts)
    input_vector = vectorize_new_text(cleaned_text, vectorizer)

    # 5. Tính độ tương đồng
    results = calculate_similarities(corpus_vectors, input_vector, corpus, top_k=top_k)

    return results
