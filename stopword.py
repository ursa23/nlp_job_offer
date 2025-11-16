import pandas as pd
import spacy
# ========================
# 1. Configuration
# ========================
#connexion base SQL
DATABASE_URI = 'postgresql://root:0000@192.168.1.120:5432/test'
QUERY = "SELECT mission_clean, profil_clean, title_clean FROM test_schema.portaljob_test LIMIT 1"
#Modèle NLP chargé
# Modèle spaCy
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    print("⚠️  Modèle spaCy 'fr_core_news_sm' non trouvé.")
    print("👉 Installez-le avec : python -m spacy download fr_core_news_sm")
    nlp = None

# Stopwords
try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('french'))
except ImportError:
    import nltk
    nltk.download('topwords')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('french'))

custom_stopwords = {
    "serait", "un", "une", "et", "de", "des", "en", "dans", "la", "le", "les", "du", "au", "aux",
    "ou", "car", "donc", "or", "ni", "par", "pour", "sur", "avec", "sans", "trop", "plus", "tres",
    "très", "cela", "ca", "ça", "ce", "mes", "tes", "ses", "son", "leur", "leurs"
}
stop_words.update(custom_stopwords)

stop_words = list(stop_words) 

print(stop_words)