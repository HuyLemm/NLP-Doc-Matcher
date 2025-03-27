from sklearn.feature_extraction.text import TfidfVectorizer

# Hàm 1: Tạo vectorizer và vector TF-IDF cho toàn bộ văn bản trong DB
def get_vectorizer_and_vectors(corpus_texts):
    if not corpus_texts or len(corpus_texts) == 0:
        raise ValueError("Corpus is empty")

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus_texts)
    return vectorizer, vectors


# Hàm 2: Vector hóa văn bản mới (văn bản upload) dựa trên vectorizer đã huấn luyện
def vectorize_new_text(text, vectorizer):
    return vectorizer.transform([text])
