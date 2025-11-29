from clean_title import df
from stopword import stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


if len(df) < 1:
    raise ValueError("📊 Pas assez de données pour effectuer un clustering.")

# converts texts into matrix
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words=stop_words,           # ✅ Maintenant un set, correct
    ngram_range=(1, 2),
    lowercase=True
)

X = vectorizer.fit_transform(df['clean_title'])


print(X)









# Déterminer le nombre optimal de clusters
def find_optimal_clusters(X, max_k=15):
    max_possible_k = min(max_k, len(df) // 2)
    if max_possible_k < 2:
        return 2
    k_range = range(2, max_possible_k + 1)
    scores = []
    for k in k_range:
        try:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            score = silhouette_score(X, kmeans.labels_)
            scores.append(score)
        except:
            scores.append(-1)  # Échec du clustering
    if not scores or all(s == -1 for s in scores):
        return 2
    best_k = k_range[scores.index(max(scores))]
    return best_k

n_clusters = find_optimal_clusters(X) if len(df) >= 10 else min(3, len(df))
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

