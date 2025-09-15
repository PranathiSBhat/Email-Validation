import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import pymysql
import pickle
import os

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",             # change if needed
        password="root",     # your MySQL password
        database="capstone_project",
        auth_plugin="mysql_native_password"
    )

def insert_prediction_to_db(email_text, nb_pred, xgb_pred):
    """Insert spam detection result into MySQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO spam_results (email_text, naive_bayes_pred, xgboost_pred)
    VALUES (%s, %s, %s)
    """
    values = (email_text, int(nb_pred), int(xgb_pred))  # store predictions as 0/1
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# Paths 
MODEL_DIR = "./ml_model"
os.makedirs(MODEL_DIR, exist_ok=True)
NB_PATH = os.path.join(MODEL_DIR, "naive_bayes_model.pkl")
XGB_PATH = os.path.join(MODEL_DIR, "xgboost_model.pkl")
VEC_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Load data
df = pd.read_csv('C:/Users/Pranathi/OneDrive/Desktop/project/uploads/validated_emails.csv')
print("data loaded")

df.info()
print("info printed")
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

print(df)

# Check distribution
print("Label distribution:\n", df['label'].value_counts())

df.head()

X = df['text'].astype(str)
y = df['label'].astype(int)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ensure text column has no NaN or empty values
X_train = X_train.dropna().astype(str)
X_train = X_train[X_train.str.strip() != ""]

X_test = X_test.dropna().astype(str)
X_test = X_test[X_test.str.strip() != ""]

# Vectorize text

if not (os.path.exists(NB_PATH) and os.path.exists(XGB_PATH) and os.path.exists(VEC_PATH)):
    print("Training models...")

    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Naive Bayes
    nb = MultinomialNB()
    nb.fit(X_train_vec, y_train)
    y_pred_nb = nb.predict(X_test_vec)
    print("Naive Bayes Results:") 
    print(classification_report(y_test, y_pred_nb))
    print("Accuracy:", accuracy_score(y_test, y_pred_nb))

    # XGBoost
    xgb = XGBClassifier(eval_metric='logloss', max_depth=3, min_child_weight=2, subsample=0.8, reg_alpha=1, reg_lambda=1)
    xgb.fit(X_train_vec, y_train)
    y_pred_xgb = xgb.predict(X_test_vec)
    print("\nXGBoost Results:")
    print(classification_report(y_test, y_pred_xgb))
    print("Accuracy:", accuracy_score(y_test, y_pred_xgb)) 

    #Saving models in .pkl file
    with open(NB_PATH, "wb") as f:
        pickle.dump(nb, f)
    with open(XGB_PATH, "wb") as f:
        pickle.dump(xgb, f)
    with open(VEC_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Models trained & saved in ./ml_model/")

else:
    print("Loading models from ./ml_model/")
    with open(NB_PATH, "rb") as f:
        nb = pickle.load(f)
    with open(XGB_PATH, "rb") as f:
        xgb = pickle.load(f)
    with open(VEC_PATH, "rb") as f:
        vectorizer = pickle.load(f)

#Evaluating the models
X_test_vec = vectorizer.transform(X_test)
print("Naive Bayes Results:")
print(classification_report(y_test, nb.predict(X_test_vec)))
print("Accuracy:", accuracy_score(y_test, nb.predict(X_test_vec)))

print("\nXGBoost Results:")
print(classification_report(y_test, xgb.predict(X_test_vec)))
print("Accuracy:", accuracy_score(y_test, xgb.predict(X_test_vec)))


# --- Prediction Function ---
def classify_and_store_email(email_text: str):
    email_vec = vectorizer.transform([email_text])
    nb_pred = nb.predict(email_vec)[0]
    xgb_pred = xgb.predict(email_vec)[0]

    insert_prediction_to_db(email_text, nb_pred, xgb_pred)

    return {
        "email_text": email_text,
        "naive_bayes_prediction": "Spam" if nb_pred == 1 else "Ham",
        "xgboost_prediction": "Spam" if xgb_pred == 1 else "Ham"
    }

# --- Main Execution ---
if __name__ == "__main__":
    user_email = input("Enter the email content/text to classify: ").strip()
    result = classify_and_store_email(user_email)

    print("\nClassification Result:")
    print("Email Text:", result["email_text"])
    print("Naive Bayes Prediction:", result["naive_bayes_prediction"])
    print("XGBoost Prediction:", result["xgboost_prediction"])