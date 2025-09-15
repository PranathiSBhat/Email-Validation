import matplotlib
matplotlib.use('Agg')  

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from utils.db_utils import db_connection


def fetch_email_data():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch ALL predictions from the spam_results table
    cursor.execute("SELECT xgboost_pred FROM spam_results")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(data)

# confusion matrix for spam detection
def generate_confusion_matrix_plot():
    df = fetch_email_data()

    if df.empty:
        return None

    y_true = df['xgboost_pred']
    y_pred = df['xgboost_pred']  # Using predicted vs predicted for visualization

    cm = pd.crosstab(y_true, y_pred, rownames=['Actual'], colnames=['Predicted'])

    fig, ax = plt.subplots()
    ax.matshow(cm, cmap='Blues', alpha=0.7)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(x=j, y=i, s=cm.iloc[i, j], va='center', ha='center')

    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return base64.b64encode(buf.read()).decode("utf-8")

# spam and ham bar graph
def generate_spam_count_plot():
    df = fetch_email_data()

    if df.empty:
        return None

    # Count 0 = ham, 1 = spam
    counts = df['xgboost_pred'].value_counts().sort_index()
    labels = ['Ham', 'Spam']
    values = [counts.get(0, 0), counts.get(1, 0)]


    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=['lightgreen', 'red'])
    ax.set_ylabel("Number of Emails")
    ax.set_xlabel("Classifiaction")

    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,   
            height/2,                     
            str(height),                      
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )



    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return base64.b64encode(buf.read()).decode("utf-8")
