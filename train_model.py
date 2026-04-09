
import os
import pickle
import nltk
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# ── Download required NLTK data ───────────────────────────────────────────────
nltk.download("movie_reviews", quiet=True)
nltk.download("punkt",         quiet=True)
nltk.download("punkt_tab",     quiet=True)   # required by NLTK 3.9+
nltk.download("stopwords",     quiet=True)

from nltk.corpus import movie_reviews, stopwords

# ── Build dataset ─────────────────────────────────────────────────────────────
def load_dataset():
    """Load NLTK movie_reviews and return (texts, labels)."""
    texts, labels = [], []
    for category in movie_reviews.categories():          # 'neg', 'pos'
        for fileid in movie_reviews.fileids(category):
            words = movie_reviews.words(fileid)
            texts.append(" ".join(words))
            labels.append(category)
    return texts, labels


# ── Custom text preprocessor ─────────────────────────────────────────────────
_stop_words = set(stopwords.words("english"))

def preprocess(text: str) -> str:
    """Lowercase, split, remove stopwords & non-alpha tokens.
    Uses split() instead of word_tokenize() to avoid punkt dependency.
    """
    tokens   = text.lower().split()
    filtered = [t for t in tokens if t.isalpha() and t not in _stop_words]
    return " ".join(filtered)


# ── Train ─────────────────────────────────────────────────────────────────────
def train():
    print("Loading dataset …")
    raw_texts, raw_labels = load_dataset()

    print("Preprocessing texts …")
    texts  = [preprocess(t) for t in raw_texts]
    le     = LabelEncoder()
    labels = le.fit_transform(raw_labels)   # neg→0, pos→1

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # TF-IDF + Logistic Regression pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=30_000,
            sublinear_tf=True,
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=1.0,
            solver="lbfgs",
        )),
    ])

    print("Training model …")
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Save artefacts
    os.makedirs("models", exist_ok=True)
    with open("models/sentiment_model.pkl", "wb") as f:
        pickle.dump(pipeline, f)
    with open("models/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    print("\nModel saved to  models/sentiment_model.pkl")
    print("Encoder saved to models/label_encoder.pkl")


if __name__ == "__main__":
    train()
