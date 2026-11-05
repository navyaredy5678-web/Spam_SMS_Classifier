import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load dataset
data = pd.read_csv("spam.csv", encoding="latin-1")

# 2. Clean column names
data.columns = data.columns.str.strip().str.lower()

print("Available columns:", data.columns.tolist())

# 3. Support both Kaggle and sample dataset formats
if "v1" in data.columns and "v2" in data.columns:
    data = data[["v1", "v2"]]
    data.columns = ["label", "message"]

elif "label" in data.columns and "message" in data.columns:
    data = data[["label", "message"]]

else:
    raise ValueError(
        "Dataset columns not recognized. "
        "Expected v1/v2 or label/message."
    )

# 4. Remove missing and duplicate records
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

# 5. Preprocess data
data["label"] = data["label"].astype(str).str.strip().str.lower()
data["message"] = data["message"].astype(str).str.strip()

data = data[data["label"].isin(["ham", "spam"])]
data = data[data["message"] != ""]

# 6. Display dataset information
print("\nTotal messages:", len(data))
print("Spam messages:", (data["label"] == "spam").sum())
print("Ham messages:", (data["label"] == "ham").sum())

if len(data) < 1000:
    print("\nWARNING: This dataset is small.")
    print("Check whether you copied the full Kaggle dataset.")

# 7. Split dataset
X = data["message"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 8. Create machine learning model
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10000
    )),
    ("classifier", MultinomialNB())
])

# 9. Train model
print("\nTraining model...")
model.fit(X_train, y_train)

# 10. Evaluate model
predictions = model.predict(X_test)

print("\nModel Accuracy:",
      round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# 11. Save model
with open("spam_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel saved successfully!")