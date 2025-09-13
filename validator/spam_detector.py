import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv('C:/CGI/Project/Email-Validation/uploads/validated_emails.csv')
df.info()
df.head()

# Remove NaN values 
df = df.dropna()

# Keep only valid labels and map: ham -> 0, spam -> 1
valid_labels = {"ham": 0, "Ham": 0, "spam": 1, "Spam": 1}
df = df[df['label'].isin(valid_labels.keys())]
df['label'] = df['label'].map(valid_labels).astype(int)

# Drop rows where text is NaN or empty
df = df.dropna(subset=['text'])
df = df[df['text'].str.strip() != ""]

# Check distribution
print("Label distribution:\n", df['label'].value_counts())

df.head()

# Drop rows where text is NaN or empty BEFORE splitting
df = df.dropna(subset=['text', 'label'])
df = df[df['text'].str.strip() != ""]

X = df['text']
y = df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ensure text column has no NaN or empty values
X_train = X_train.dropna().astype(str)
X_train = X_train[X_train.str.strip() != ""]

X_test = X_test.dropna().astype(str)
X_test = X_test[X_test.str.strip() != ""]

# Vectorize text
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# XGBoost
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', max_depth=3, min_child_weight=2, subsample=0.8, reg_alpha=1, reg_lambda=1)
xgb.fit(X_train_vec, y_train)
y_pred_xgb = xgb.predict(X_test_vec)
print("\nXGBoost Results:")
print(classification_report(y_test, y_pred_xgb))
print("Accuracy:", accuracy_score(y_test, y_pred_xgb))

import pickle

# Save the XGBoost model inside the models folder
with open('C:/Users/Pranathi/OneDrive/Desktop/project/ml_model/spam_model.pkl', 'wb') as model_file:
    pickle.dump(xgb, model_file)

# Save the TF-IDF vectorizer inside the models folder
with open('C:/Users/Pranathi/OneDrive/Desktop/project/ml_model/tfidf_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print("Model and vectorizer saved successfully to the models/ folder using pickle!")

