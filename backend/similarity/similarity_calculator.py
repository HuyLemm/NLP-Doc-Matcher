from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarities(corpus_vectors, input_vector, metadata, top_k=5):
    similarities = cosine_similarity(input_vector, corpus_vectors)[0]  # shape: (n,)
    
    results = []
    for i, score in enumerate(similarities):
        if score is None or isinstance(score, float) == False:
            score = 0.0  # tránh NaN

        results.append({
            "source": metadata[i].get("source", "Không rõ"),
            "category": metadata[i].get("category", "Không rõ"),
            "text": metadata[i].get("text", "")[:500],  # Giới hạn hiển thị
            "similarity": round(float(score), 4)
        })

    # Sắp xếp giảm dần theo similarity
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
