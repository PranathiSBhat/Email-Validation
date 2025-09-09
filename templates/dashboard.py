import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# --- Page Config ---
st.set_page_config(layout="wide", page_title="Email Validation Dashboard", page_icon="✅")

# --- Sidebar ---
with st.sidebar:
    st.title("Email Validation")
    st.markdown("---")
    st.header("Navigation")
    st.button("Dashboard", use_container_width=True)
    st.button("Validation", use_container_width=True)
    st.button("History", use_container_width=True)
    st.button("Reports", use_container_width=True)
    st.markdown("---")
    st.markdown("`_Powered by Streamlit_`")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# --- Header ---
st.title("Email Validation Dashboard")
st.markdown("---")

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Ensure column names
    df = df.rename(columns={df.columns[0]: "Text", df.columns[1]: "Status"})
    status_map = {1: "Spam", 0: "Not Spam"}
    df["Status"] = df["Status"].map(status_map).fillna("Unknown")

    # --- Extract domain if email addresses are in Text ---
    df["Domain"] = df["Text"].apply(lambda x: x.split("@")[1] if "@" in x else "Unknown")

    # --- Show Data ---
    st.subheader("Uploaded Data (Last 10 rows)")
    st.dataframe(df[["Text", "Status", "Domain"]].tail(10), use_container_width=True, hide_index=True)

    # --- Summary Metrics ---
    st.subheader("Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Emails", df.shape[0])
    col2.metric("Spam Emails", df[df["Status"] == "Spam"].shape[0])
    col3.metric("Non-Spam Emails", df[df["Status"] == "Not Spam"].shape[0])
    col4.metric("Unknown Status", df[df["Status"] == "Unknown"].shape[0])

    # --- Spam vs Non-Spam Pie Chart ---
    st.subheader("Spam vs Non-Spam Distribution")
    pie_fig = px.pie(df, names="Status", title="Spam Distribution", color="Status",
                     color_discrete_map={"Spam": "red", "Not Spam": "green", "Unknown": "gray"})
    st.plotly_chart(pie_fig, use_container_width=True)

    # --- Email Status Counts Bar Chart ---
    st.subheader("Email Status Counts")
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    status_count_fig = px.bar(
        status_counts,
        x="Status",
        y="Count",
        color="Status",
        color_discrete_map={"Spam": "red", "Not Spam": "green", "Unknown": "gray"},
        labels={"Count": "Number of Emails"},
        title="Email Status Counts"
    )
    st.plotly_chart(status_count_fig, use_container_width=True)

    # --- Domain Distribution ---
    st.subheader("Email Distribution by Domain")
    domain_counts = df['Domain'].value_counts().reset_index()
    domain_counts.columns = ['Domain', 'Count']
    domain_bar = px.bar(domain_counts, x='Domain', y='Count', title='Emails by Domain',
                        color='Count', color_continuous_scale='Viridis')
    st.plotly_chart(domain_bar, use_container_width=True)

    # --- Top Words in Spam Emails ---
    st.subheader("Top Words in Spam Emails")
    spam_texts = df[df["Status"] == "Spam"]["Text"].tolist()
    words = []
    for text in spam_texts:
        words.extend(re.findall(r'\w+', text.lower()))
    top_words = Counter(words).most_common(10)
    top_words_df = pd.DataFrame(top_words, columns=["Word", "Count"])
    st.bar_chart(top_words_df.set_index("Word"))

    # --- Email Length Analysis ---
    st.subheader("Email Length Distribution")
    df["Length"] = df["Text"].apply(len)
    length_fig = px.histogram(df, x="Length", color="Status", nbins=30,
                              color_discrete_map={"Spam": "red", "Not Spam": "green", "Unknown": "gray"},
                              title="Email Length Distribution by Status")
    st.plotly_chart(length_fig, use_container_width=True)
