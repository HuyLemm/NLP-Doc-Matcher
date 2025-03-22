import unicodedata

def normalize_text(text):
    """Chuyển văn bản về chữ thường không dấu để so sánh"""
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()