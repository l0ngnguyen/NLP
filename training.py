import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from models import ArticleDB
from nlp import remove_number
from utils import load_stopwords, load_yaml


def load_data():
    db = ArticleDB()
    label_names = load_yaml("labels")
    session = db.create_session()

    data = db.get_articles_by_specific_categories(session, label_names)
    df = pd.DataFrame(data, columns=["id", "category", "text"])

    return df


def svm_straing(X_train, y_train):
    print("start training")
    PATHS = load_yaml("paths")

    text_clf = Pipeline(
        [
            (
                "vect",
                TfidfVectorizer(
                    max_features=50000,
                    lowercase=False,
                    min_df=1,
                    stop_words=None,
                    preprocessor=remove_number,
                ),
            ),
            ("clf", LinearSVC()),
        ]
    )
    text_clf = text_clf.fit(X_train, y_train)
    # Save model
    pickle.dump(text_clf, open(PATHS["model"], "wb"))
    return text_clf
