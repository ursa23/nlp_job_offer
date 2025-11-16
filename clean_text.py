import pandas as pd
from sqlalchemy import create_engine
import re
# ========================
# 2. Charger les données
# ========================

DATABASE_URI = 'postgresql://root:0000@192.168.1.120:5432/test'
QUERY = "SELECT mission_clean, profil_clean, title_clean FROM test_schema.portaljob_test LIMIT 1"


engine = create_engine(DATABASE_URI)
try:
    df = pd.read_sql_query(QUERY, engine)
    print(f"✅ {len(df)} lignes récupérées de la base de données.")
except Exception as e:
    raise Exception(f"❌ Erreur lors de la requête SQL : {e}")

# Nettoyage de base
df.dropna(subset=['title_clean'], inplace=True)
df = df[df['title_clean'].astype(str).str.len() > 2]


# def clean_text_old(text: str) -> str:
#     if not isinstance(text, str):
#         return ""
#     text = text.lower()
#     text = re.sub(r"[^a-zàâäéèêëîïôöùûüç\s]", " ", text)  # garder lettres + accents
#     text = re.sub(r"\s+", " ", text).strip()
#     return text

def clean_text(text: str) -> str:
    """
    Nettoie un texte pour préparer le matching avec keyword_mapping.
    - Convertit en minuscules
    - Supprime la ponctuation (sauf les accents et espaces)
    - Normalise les espaces
    - Préserve les termes composés courants (ex: "data scientist", "ui ux", "supply chain")
    """
    if not isinstance(text, str):
        return ""

    # 1. Conversion en minuscules
    text= text.lower()

    # 2. Remplacer les tirets, underscores, slash par des espaces (pour séparer les mots)
    # mais conserver les termes composés courants en les normalisant d'abord
    text = re.sub(r"[-_/]", " ", text)

    # 3. Supprimer tout ce qui n’est pas une lettre (avec accents), un espace, ou un chiffre (optionnel)
    # → On garde les chiffres si vous avez des termes comme "bac+2", "caces 3", etc.
    text = re.sub(r"[^a-zàâäéèêëîïôöùûüç0-9\s]", " ", text)

    # 4. Normaliser les espaces multiples
    text = re.sub(r"\s+", " ", text).strip()

    # 5. [OPTION STRATÉGIQUE] Préserver les bigrammes/trigrammes clés en remplaçant l'espace par un tiret bas
    # Ex: "data scientist" → "data_scientist" pour matcher exactement dans keyword_mapping
    # → À faire APRÈS le nettoyage, et seulement si votre matching gère les underscores
    # → Sinon, laissez en espace — mais adaptez votre matching en conséquence.

    return text


# def addition(a,b) :
#     sum = a + b

#     print(sum)

if __name__ == "__main__":
    print("hello")
    clean = clean_text("     ça vé    SARAH ah!!!")
    print(clean)
    # add1= addition(1,2)
    # print(add1)
    # # addition(add1,2)
